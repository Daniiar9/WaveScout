from __future__ import annotations

from app.models import AudienceProfile, CommentSignal, CreatorCandidate, CreatorContentSample, CreatorFitScore, TrendWave
from app.services.audience_analysis import infer_audience_profile
from app.services.comment_intelligence import calculate_comment_intent_quality
from app.services.creator_content_analysis import summarize_creator_content
from app.services.text import weighted_overlap


def score_creator_for_wave(
    creator: CreatorCandidate,
    trend_wave: TrendWave,
    content_samples: list[CreatorContentSample],
    comment_signals: list[CommentSignal],
    product_context: str,
    audience_profile: AudienceProfile | None = None,
    content_summary: dict | None = None,
) -> CreatorFitScore:
    audience_profile = audience_profile or infer_audience_profile(creator, content_samples, comment_signals, product_context)
    content_summary = content_summary or summarize_creator_content(creator, content_samples)
    topical = _topical_relevance(creator, trend_wave, content_samples)
    audience = round(audience_profile.audience_fit_score * 0.25)
    comment_quality = calculate_comment_intent_quality(comment_signals)
    trust = int(content_summary["trust_and_clarity"]["score"])
    demo_fit = _product_demo_fit(content_samples, content_summary)
    commercial = _commercial_priority(creator)
    risks = _risks(creator, audience_profile, content_summary, topical, comment_quality)
    risk_penalty = -min(20, sum(item[0] for item in risks))
    total = max(0, min(100, topical + audience + comment_quality + trust + demo_fit + commercial + risk_penalty))
    fit_level = _fit_level(total, risks)
    reasons = _reasons(creator, topical, audience_profile, comment_quality, content_summary, demo_fit, commercial)
    best_angle = _best_angle(content_summary, audience_profile, trend_wave)
    suggested_offer = (
        "Offer product access plus a short founder walkthrough for a human-reviewed concept."
        if fit_level in {"high", "medium"}
        else "Do not contact until more relevant evidence is imported."
    )
    outreach_priority = "priority_review" if fit_level == "high" else "review_later" if fit_level == "medium" else "hold"
    return CreatorFitScore(
        creator_id=creator.id,
        trend_wave_id=trend_wave.id,
        score=total,
        fit_level=fit_level,
        topical_relevance=topical,
        audience_relevance=audience,
        comment_intent_quality=comment_quality,
        creator_trust_clarity=trust,
        product_demo_fit=demo_fit,
        commercial_priority=commercial,
        risk_penalty=risk_penalty,
        reasons=reasons,
        risks=[risk for _points, risk in risks],
        best_angle=best_angle,
        suggested_offer=suggested_offer,
        outreach_priority=outreach_priority,
    )


def _topical_relevance(
    creator: CreatorCandidate,
    trend_wave: TrendWave,
    content_samples: list[CreatorContentSample],
) -> int:
    wave_terms = trend_wave.keywords + trend_wave.hashtags + trend_wave.adjacent_topics + [trend_wave.name, trend_wave.category]
    creator_text = " ".join(
        [
            creator.bio,
            " ".join(creator.categories),
            " ".join(creator.hashtags_used),
            " ".join(creator.recent_video_summaries),
            " ".join(sample.title_or_caption + " " + sample.transcript_or_summary + " " + " ".join(sample.topics) for sample in content_samples),
        ]
    )
    overlap = weighted_overlap(wave_terms, creator_text)
    return min(20, overlap * 4)


def _product_demo_fit(content_samples: list[CreatorContentSample], content_summary: dict) -> int:
    formats = set(content_summary.get("formats", []))
    score = 0
    if formats & {"demo", "tutorial", "teardown"}:
        score += 6
    if formats & {"comparison", "founder_pov", "news_commentary"}:
        score += 3
    if len(content_summary.get("themes", [])) >= 4:
        score += 1
    return min(10, score)


def _commercial_priority(creator: CreatorCandidate) -> int:
    score = 0
    if creator.email_or_contact:
        score += 3
    if creator.avg_views >= 25_000:
        score += 3
    elif creator.avg_views >= 5_000:
        score += 2
    if creator.follower_count >= 100_000:
        score += 2
    elif creator.follower_count >= 10_000:
        score += 1
    if "agency" in " ".join(creator.categories).lower() or "founder" in creator.bio.lower():
        score += 2
    return min(10, score)


def _risks(
    creator: CreatorCandidate,
    audience_profile: AudienceProfile,
    content_summary: dict,
    topical: int,
    comment_quality: int,
) -> list[tuple[int, str]]:
    risks: list[tuple[int, str]] = []
    creator_text = " ".join([creator.bio, " ".join(creator.categories), creator.engagement_notes]).lower()
    if topical < 8:
        risks.append((12, "Topic mismatch with the trend wave."))
    if comment_quality < 5:
        risks.append((8, "Comment intent is weak or mostly generic hype."))
    if audience_profile.audience_quality_level in {"low_quality", "irrelevant"}:
        risks.append((12, "Audience appears low quality or unrelated to the product buyer."))
    if any(term in creator_text for term in ["spam", "follow for follow", "giveaway only"]):
        risks.append((12, "Creator has spammy positioning signals."))
    if "competitor-heavy" in creator_text:
        risks.append((8, "Positioning appears competitor-heavy."))
    if content_summary.get("sample_count", 0) == 0:
        risks.append((5, "Missing imported content samples."))
    if content_summary.get("trust_and_clarity", {}).get("hype_level") == "high":
        risks.append((6, "Creator style may overpromise or lean on hype."))
    return risks


def _fit_level(score: int, risks: list[tuple[int, str]]) -> str:
    severe_risk = any(points >= 12 for points, _risk in risks)
    if severe_risk and score < 65:
        return "reject"
    if score >= 78:
        return "high"
    if score >= 58:
        return "medium"
    if score >= 40:
        return "low"
    return "reject"


def _reasons(
    creator: CreatorCandidate,
    topical: int,
    audience_profile: AudienceProfile,
    comment_quality: int,
    content_summary: dict,
    demo_fit: int,
    commercial: int,
) -> list[str]:
    reasons: list[str] = []
    if topical >= 14:
        reasons.append("Content topics map closely to the trend wave.")
    if audience_profile.audience_fit_score >= 70:
        reasons.append("Audience profile contains likely product users or buyers.")
    if comment_quality >= 12:
        reasons.append("Comments include implementation-level questions and use cases.")
    if content_summary["trust_and_clarity"]["score"] >= 10:
        reasons.append("Creator style appears clear enough for a credible product explanation.")
    if demo_fit >= 7:
        reasons.append("Existing content format can naturally support a product demo or teardown.")
    if commercial >= 6:
        reasons.append("Creator has usable commercial/contact signals without overvaluing reach.")
    if not reasons:
        reasons.append("Imported evidence is limited or weak for this wave.")
    return reasons


def _best_angle(content_summary: dict, audience_profile: AudienceProfile, trend_wave: TrendWave) -> str:
    if audience_profile.tool_mentions:
        return f"Show how one question can pull context from {', '.join(audience_profile.tool_mentions[:2])}."
    if "tutorial" in content_summary.get("formats", []):
        return "Walk through one real workflow from scattered SaaS context to an answer."
    if "teardown" in content_summary.get("formats", []):
        return "Teardown why app data gets trapped and how a connected workspace changes the loop."
    return f"Explain the {trend_wave.name} wave through a concrete daily workflow."

