from __future__ import annotations

from app.models import AudienceProfile, ContentAngle, CreatorCandidate, TrendWave
from app.services.text import stable_id, unique_keep_order


BASE_ANGLES = [
    "Stop opening 12 SaaS tabs to answer one business question",
    "What if your SaaS stack had one brain?",
    "I asked my apps one question and got the workflow back",
    "This is what comes after vibe coding",
    "Your apps have data. The problem is they do not talk to each other.",
]


def generate_content_angles(
    product_context: str,
    trend_wave: TrendWave,
    creator: CreatorCandidate,
    content_summary: dict,
    audience_profile: AudienceProfile,
    comment_intelligence_summary: dict,
    limit: int = 5,
) -> list[ContentAngle]:
    themes = content_summary.get("themes", [])
    formats = content_summary.get("formats", ["demo"])
    top_questions = comment_intelligence_summary.get("common_questions", [])
    titles = list(BASE_ANGLES)
    if audience_profile.tool_mentions:
        titles.insert(0, f"Can one AI workspace answer questions across {audience_profile.tool_mentions[0]} and the rest of your stack?")
    if top_questions:
        titles.insert(0, f"Answering the comment: {top_questions[0].rstrip('?')}?")
    titles = unique_keep_order(titles, limit)
    angles: list[ContentAngle] = []
    for index, title in enumerate(titles):
        content_format = formats[0] if formats else "demo"
        angle = ContentAngle(
            id=stable_id("angle", creator.id, trend_wave.id, title),
            creator_id=creator.id,
            trend_wave_id=trend_wave.id,
            title=title,
            hook=title,
            short_script=_short_script(title, product_context, themes),
            why_it_fits_wave=f"Connects the {trend_wave.name} wave to a specific workflow pain instead of generic AI hype.",
            product_mention_style="Mention as a product to inspect, not as something the creator already uses.",
            creator_prompt=f"Use your natural {content_format} format and test one practical question across the stack.",
            avoid_saying=[
                "AI will replace everything",
                "This fully automates your company",
                "The creator already uses the product",
                "Guaranteed productivity gains",
            ],
            hashtags=unique_keep_order(trend_wave.hashtags + creator.hashtags_used, 6),
            format=content_format if content_format != "unknown" else "demo",
            confidence=max(0.35, 0.85 - (index * 0.08)),
        )
        angles.append(angle)
    return angles


def _short_script(title: str, product_context: str, themes: list[str]) -> str:
    theme_line = f" Tie it to {', '.join(themes[:2])}." if themes else ""
    product_phrase = _lower_first(product_context).rstrip(".")
    return (
        f"Open with: '{title}'. Show the before state: scattered app context. "
        f"Then show how {product_phrase} helps answer one specific question and turn it into a next step."
        f"{theme_line}"
    )


def _lower_first(value: str) -> str:
    return value[:1].lower() + value[1:] if value else value
