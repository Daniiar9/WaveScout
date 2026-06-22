from __future__ import annotations

from app.models import CreatorSearchStrategy, OwnedTikTokProfile, ProductIntelligenceBrief, TrendWaveMap
from app.services.text import stable_id, unique_keep_order


def build_creator_search_strategy(
    product_brief: ProductIntelligenceBrief,
    wave_map: TrendWaveMap,
    owned_profile: OwnedTikTokProfile | None = None,
) -> CreatorSearchStrategy:
    return CreatorSearchStrategy(
        id=stable_id("strategy", product_brief.id),
        product_id=product_brief.id,
        trend_waves=wave_map.primary_waves + wave_map.adjacent_waves,
        creator_archetypes=generate_creator_archetypes(product_brief, wave_map, owned_profile),
        search_queries=generate_search_queries(product_brief, wave_map, owned_profile),
        hashtags=generate_hashtag_targets(product_brief, wave_map),
        keywords=unique_keep_order(wave_map.search_keywords + product_brief.trend_keywords, 20),
        content_formats_to_target=["demo", "tutorial", "teardown", "comparison", "founder_pov"],
        comment_patterns_to_look_for=generate_comment_patterns(product_brief),
        qualification_criteria=generate_qualification_criteria(product_brief),
        rejection_criteria=generate_rejection_criteria(product_brief),
        outreach_angles=product_brief.creator_relevant_angles,
        priority_order=[
            "Search high-intent workflow demo creators first",
            "Prioritize creators with implementation-level comments",
            "Build packets for the top qualified creators",
            "Human-review proposals before manual outreach",
        ],
    )


def generate_search_queries(
    product_brief: ProductIntelligenceBrief,
    wave_map: TrendWaveMap,
    owned_profile: OwnedTikTokProfile | None = None,
) -> list[str]:
    queries = []
    for wave in wave_map.primary_waves[:5]:
        queries.append(f'TikTok creators "{wave}"')
        queries.append(f'"{wave}" demo creator')
    for archetype in wave_map.creator_archetypes[:6]:
        queries.append(f"TikTok {archetype}")
    if owned_profile:
        for theme in owned_profile.content_themes[:3]:
            queries.append(f"creators making videos about {theme}")
    return unique_keep_order(queries, 24)


def generate_hashtag_targets(product_brief: ProductIntelligenceBrief, wave_map: TrendWaveMap) -> list[str]:
    return unique_keep_order(wave_map.hashtags + ["#NoCode", "#FounderTools", "#StartupTools"], 14)


def generate_creator_archetypes(
    product_brief: ProductIntelligenceBrief,
    wave_map: TrendWaveMap,
    owned_profile: OwnedTikTokProfile | None = None,
) -> list[str]:
    archetypes = list(wave_map.creator_archetypes)
    if owned_profile and "tutorial" in owned_profile.top_formats:
        archetypes.insert(0, "tutorial-first product educators")
    return unique_keep_order(archetypes, 12)


def generate_comment_patterns(product_brief: ProductIntelligenceBrief) -> list[str]:
    return [
        "Can this connect to Notion?",
        "Does it work with Slack?",
        "I need this for my CRM.",
        "Can you make a tutorial?",
        "How would this work for a small agency?",
        "Is this real or just a demo?",
    ]


def generate_qualification_criteria(product_brief: ProductIntelligenceBrief) -> list[str]:
    return [
        "content matches wave",
        "audience has buyer/user intent",
        "comments ask implementation questions",
        "creator explains tools clearly",
        "product angle feels native",
        "low spam/hype risk",
    ]


def generate_rejection_criteria(product_brief: ProductIntelligenceBrief) -> list[str]:
    return [
        "generic AI hype only",
        "unrelated audience",
        "mostly meme/reaction content",
        "no implementation comments",
        "competitor-heavy with poor fit",
        "creator style would misrepresent product",
    ]


def render_search_strategy_markdown(strategy: CreatorSearchStrategy) -> str:
    return f"""# Creator Search Strategy

## Creator Archetypes
{_bullets(strategy.creator_archetypes)}

## Search Queries
{_bullets(strategy.search_queries)}

## Hashtags
{_bullets(strategy.hashtags)}

## Comment Patterns To Look For
{_bullets(strategy.comment_patterns_to_look_for)}

## Qualification Criteria
{_bullets(strategy.qualification_criteria)}

## Rejection Criteria
{_bullets(strategy.rejection_criteria)}

## Outreach Angles
{_bullets(strategy.outreach_angles)}

## Priority Order
{_bullets(strategy.priority_order)}
"""


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)

