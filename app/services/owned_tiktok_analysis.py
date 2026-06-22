from __future__ import annotations

from app.models import CreatorContentSample, OwnedTikTokProfile, ProductIntelligenceBrief
from app.services.comment_intelligence import extract_comment_signals, summarize_comment_intelligence
from app.services.creator_content_analysis import extract_content_themes, identify_creator_formats
from app.services.text import normalize_handle, unique_keep_order


def analyze_owned_tiktok_profile(
    handle: str,
    content_samples: list[CreatorContentSample] | None = None,
    comments: list[str | dict] | None = None,
) -> OwnedTikTokProfile:
    content_samples = content_samples or []
    comments = comments or []
    signals = extract_comment_signals(comments, normalize_handle(handle)) if comments else []
    comment_summary = summarize_comment_intelligence(signals)
    return OwnedTikTokProfile(
        handle=normalize_handle(handle),
        profile_url=f"https://www.tiktok.com/{normalize_handle(handle)}" if handle else "",
        content_themes=extract_content_themes(content_samples),
        top_hooks=identify_top_hooks(content_samples),
        top_formats=identify_top_formats(content_samples),
        audience_questions=comment_summary.get("common_questions", []),
        audience_pains=comment_summary.get("common_pains", []),
        comment_intelligence_summary=comment_summary,
        brand_voice_notes=infer_brand_voice(content_samples),
        best_performing_angles=identify_top_hooks(content_samples)[:5],
        avoid_repeating=["Generic AI hype", "Unsupported automation claims"],
        confidence=0.75 if content_samples or comments else 0.35,
    )


def infer_brand_voice(content_samples: list[CreatorContentSample]) -> list[str]:
    if not content_samples:
        return ["No owned content imported; use manual review before assuming brand voice."]
    formats = identify_creator_formats(content_samples)
    notes = ["Practical and workflow-oriented" if "demo" in formats or "tutorial" in formats else "Needs more owned content evidence"]
    return notes


def identify_top_hooks(content_samples: list[CreatorContentSample]) -> list[str]:
    hooks = [sample.title_or_caption for sample in content_samples if sample.title_or_caption]
    return unique_keep_order(hooks, 8)


def identify_top_formats(content_samples: list[CreatorContentSample]) -> list[str]:
    return identify_creator_formats(content_samples)


def summarize_owned_audience_comments(comments: list[str | dict]) -> dict:
    return summarize_comment_intelligence(extract_comment_signals(comments, "owned"))


def identify_content_gaps(product_brief: ProductIntelligenceBrief, owned_profile: OwnedTikTokProfile) -> list[str]:
    gaps = []
    for angle in product_brief.creator_relevant_angles[:5]:
        if not any(angle.lower() in hook.lower() for hook in owned_profile.top_hooks):
            gaps.append(angle)
    return gaps or ["No obvious gaps from imported content."]


def identify_creator_collab_opportunities(product_brief: ProductIntelligenceBrief, owned_profile: OwnedTikTokProfile) -> list[str]:
    return [
        f"Ask creators to remix: {angle}"
        for angle in product_brief.creator_relevant_angles[:4]
    ]


def render_owned_tiktok_profile_markdown(profile: OwnedTikTokProfile) -> str:
    return f"""# Owned TikTok Account Intelligence

## Profile
- Handle: {profile.handle}
- URL: {profile.profile_url}
- Confidence: {profile.confidence}

## Content Themes
{_bullets(profile.content_themes)}

## Top Hooks
{_bullets(profile.top_hooks)}

## Top Formats
{_bullets(profile.top_formats)}

## Audience Questions
{_bullets(profile.audience_questions)}

## Audience Pains
{_bullets(profile.audience_pains)}

## Content Gaps
{_bullets(profile.content_gaps)}

## Creator Collab Opportunities
{_bullets(profile.creator_collab_opportunities)}

## Brand Voice Notes
{_bullets(profile.brand_voice_notes)}
"""


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)

