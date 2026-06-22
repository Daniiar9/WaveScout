from __future__ import annotations

from app.models import GrowthBrief
from app.services.creator_search_strategy import render_search_strategy_markdown
from app.services.discovery_provider_service import render_candidate_shortlist_markdown
from app.services.notion_pipeline_builder import render_notion_pipeline_markdown
from app.services.owned_tiktok_analysis import render_owned_tiktok_profile_markdown
from app.services.outreach_packet_builder import render_creator_packet_markdown
from app.services.product_intelligence import render_product_brief_markdown
from app.services.trend_wave_mapper import render_trend_wave_map_markdown


def render_growth_brief_markdown(growth_brief: GrowthBrief) -> str:
    top_candidates = ", ".join(candidate.handle for candidate in growth_brief.candidate_shortlist[:5]) or "None yet"
    owned = (
        render_owned_tiktok_profile_markdown(growth_brief.owned_tiktok_profile)
        if growth_brief.owned_tiktok_profile
        else "No owned TikTok profile provided."
    )
    packets = "\n\n".join(render_creator_packet_markdown(packet) for packet in growth_brief.top_creator_packets)
    return f"""# WaveScout Growth Brief

## Executive Summary

- Product: {growth_brief.product_brief.one_liner}
- Category: {growth_brief.product_brief.category}
- Primary trend waves: {", ".join(growth_brief.wave_map.primary_waves[:6])}
- Creator archetypes: {", ".join(growth_brief.search_strategy.creator_archetypes[:6])}
- Discovery mode: dry-run
- Top candidates: {top_candidates}
- Safety status: external_calls=false, tiktok_scraping=false, tiktok_dm_send=false, live_post=false

## Product Intelligence

{render_product_brief_markdown(growth_brief.product_brief)}

## Trend Wave Map

{render_trend_wave_map_markdown(growth_brief.wave_map)}

## Creator Search Strategy

{render_search_strategy_markdown(growth_brief.search_strategy)}

## Owned TikTok Intelligence

{owned}

## Discovery Provider Results

{_discovery_summary(growth_brief.discovery_summary)}

## Candidate Shortlist

{render_candidate_shortlist_markdown(growth_brief.candidate_shortlist)}

## Creator Intelligence Packets

{packets or "No scored creator packets yet. Import creator content/comments to enrich candidates."}

## Content Angles To Test

{_bullets(growth_brief.content_recommendations)}

## Outreach Recommendations

{_bullets(growth_brief.outreach_recommendations)}

## Notion Dry-Run Pipeline

{render_notion_pipeline_markdown(growth_brief.notion_pipeline_payload)}

## Missing Data

{_bullets(growth_brief.missing_data)}

## Next Safe Actions

{_bullets(growth_brief.next_safe_actions)}

## Safety Status

{_safety_lines(growth_brief.safety_status)}
"""


def _discovery_summary(summary: dict) -> str:
    rows = ["| Metric | Value |", "|---|---|"]
    for key, value in summary.items():
        rows.append(f"| {key} | {value} |")
    return "\n".join(rows)


def _safety_lines(status: dict) -> str:
    return "\n".join(f"- {key}={str(value).lower()}" for key, value in status.items())


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)

