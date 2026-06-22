from __future__ import annotations

from app.models import ProductIntelligenceBrief, TrendWaveMap
from app.services.text import stable_id, unique_keep_order


def build_trend_wave_map(product_brief: ProductIntelligenceBrief) -> TrendWaveMap:
    primary = generate_wave_keywords(product_brief)
    adjacent = _adjacent_waves(product_brief)
    rejected = reject_bad_waves(product_brief)
    reasons = {wave: f"Matches {product_brief.category} pain points and creator education format." for wave in primary}
    return TrendWaveMap(
        id=stable_id("wave_map", product_brief.id),
        product_id=product_brief.id,
        primary_waves=primary,
        adjacent_waves=adjacent,
        rejected_waves=rejected,
        wave_relevance_reasons=reasons,
        hashtags=generate_wave_hashtags(product_brief),
        search_keywords=unique_keep_order(product_brief.trend_keywords + primary + adjacent, 18),
        creator_archetypes=identify_creator_archetypes(product_brief),
        why_now="Creators are moving from generic AI tips to specific workflow demos and practical operator use cases.",
        confidence=min(0.9, product_brief.confidence + 0.05),
    )


def generate_wave_keywords(product_brief: ProductIntelligenceBrief) -> list[str]:
    if "AI workspace" in product_brief.category:
        return [
            "talk to your apps",
            "AI workspace",
            "connected SaaS stack",
            "AI agents for operators",
            "RevOps automation",
            "workflow automation",
        ]
    return unique_keep_order(product_brief.trend_keywords, 8)


def generate_wave_hashtags(product_brief: ProductIntelligenceBrief) -> list[str]:
    hashtags = ["#AIWorkspace", "#Automation", "#SaaS", "#AIAgents", "#RevOps"]
    for keyword in product_brief.trend_keywords:
        tag = "#" + "".join(part.capitalize() for part in keyword.replace("/", " ").split()[:3])
        hashtags.append(tag)
    return unique_keep_order(hashtags, 12)


def identify_creator_archetypes(product_brief: ProductIntelligenceBrief) -> list[str]:
    archetypes = [
        "AI workflow demo creators",
        "vibe-coding builders",
        "no-code app builders",
        "RevOps/operator creators",
        "founder productivity creators",
        "SaaS stack teardown creators",
        "AI agents tutorial creators",
        "startup automation creators",
        "tech stack reviewers",
    ]
    if "developers" in product_brief.target_users:
        archetypes.insert(1, "developer tool builders")
    return unique_keep_order(archetypes, 12)


def reject_bad_waves(product_brief: ProductIntelligenceBrief) -> list[str]:
    return [
        "generic ChatGPT tips",
        "AI girlfriend",
        "AI image trends",
        "unrelated productivity hacks",
        "crypto hype",
        "fitness/lifestyle AI",
    ]


def render_trend_wave_map_markdown(wave_map: TrendWaveMap) -> str:
    return f"""# Trend Wave Map

## Primary Waves
{_bullets(wave_map.primary_waves)}

## Adjacent Waves
{_bullets(wave_map.adjacent_waves)}

## Rejected Waves
{_bullets(wave_map.rejected_waves)}

## Hashtags
{_bullets(wave_map.hashtags)}

## Search Keywords
{_bullets(wave_map.search_keywords)}

## Creator Archetypes
{_bullets(wave_map.creator_archetypes)}

## Why Now
{wave_map.why_now}
"""


def _adjacent_waves(product_brief: ProductIntelligenceBrief) -> list[str]:
    return [
        "vibe coding",
        "no-code app builders",
        "founder productivity",
        "personal AI chief of staff",
        "SaaS stack cleanup",
        "AI automations for agencies",
    ]


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)

