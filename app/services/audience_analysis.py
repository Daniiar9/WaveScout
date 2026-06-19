from __future__ import annotations

from app.models import AudienceProfile, CommentSignal, CreatorCandidate, CreatorContentSample
from app.services.comment_intelligence import summarize_comment_intelligence
from app.services.text import unique_keep_order


SEGMENT_KEYWORDS = {
    "founders": ["founder", "startup", "build in public", "saas"],
    "builders": ["builder", "agent", "workflow", "automation", "vibe code", "nocode"],
    "RevOps/operators": ["revops", "crm", "operator", "sales ops", "hubspot", "pipeline"],
    "students": ["student", "class", "school", "learn"],
    "AI tourists": ["chatgpt tips", "ai hacks", "viral ai", "crazy ai"],
    "agency owners": ["agency", "client", "small agency"],
    "other creators": ["creator", "duet", "collab"],
    "developers": ["developer", "code", "api", "github"],
    "SMB owners": ["small business", "smb", "owner"],
    "enterprise buyers": ["enterprise", "procurement", "security", "admin"],
    "irrelevant/general": ["fitness", "gym", "fashion", "food", "travel"],
}


def infer_audience_profile(
    creator: CreatorCandidate,
    content_samples: list[CreatorContentSample],
    comment_signals: list[CommentSignal],
    product_context: str,
) -> AudienceProfile:
    combined = " ".join(
        [
            creator.bio,
            " ".join(creator.categories),
            " ".join(creator.hashtags_used),
            " ".join(sample.title_or_caption + " " + sample.transcript_or_summary for sample in content_samples),
            " ".join(signal.comment_text for signal in comment_signals),
            product_context,
        ]
    ).lower()
    segments: list[str] = []
    for segment, keywords in SEGMENT_KEYWORDS.items():
        if any(keyword in combined for keyword in keywords):
            segments.append(segment)
    if not segments:
        segments.append("irrelevant/general")

    comment_summary = summarize_comment_intelligence(comment_signals)
    profile = AudienceProfile(
        creator_id=creator.id,
        likely_audience_segments=unique_keep_order(segments, 5),
        buyer_intent_summary=comment_summary["summary"],
        common_questions=comment_summary["common_questions"],
        common_pains=comment_summary["common_pains"],
        objections=comment_summary["objections"],
        tool_mentions=comment_summary["tool_mentions"],
        audience_quality_level=_audience_quality(comment_summary, segments),
        confidence=0.75 if comment_signals and content_samples else 0.45,
    )
    profile.audience_fit_score = score_audience_fit(profile, product_context)
    return profile


def score_audience_fit(audience_profile: AudienceProfile, product_context: str) -> int:
    high_value = {"founders", "builders", "RevOps/operators", "agency owners", "developers", "SMB owners"}
    awareness = {"AI tourists", "students", "other creators", "enterprise buyers"}
    score = 0
    score += sum(16 for segment in audience_profile.likely_audience_segments if segment in high_value)
    score += sum(7 for segment in audience_profile.likely_audience_segments if segment in awareness)
    score += min(20, len(audience_profile.common_questions) * 4)
    score += min(20, len(audience_profile.common_pains) * 5)
    score += min(15, len(audience_profile.tool_mentions) * 5)
    if audience_profile.audience_quality_level == "high_intent":
        score += 15
    elif audience_profile.audience_quality_level == "useful_awareness":
        score += 8
    elif audience_profile.audience_quality_level in {"low_quality", "irrelevant"}:
        score -= 20
    return max(0, min(100, score))


def _audience_quality(comment_summary: dict, segments: list[str]) -> str:
    if "irrelevant/general" in segments and len(segments) == 1:
        return "irrelevant"
    if comment_summary["quality"] == "high":
        return "high_intent"
    if comment_summary["quality"] == "medium":
        return "useful_awareness"
    if comment_summary["quality"] == "low":
        return "low_quality"
    return "mixed"

