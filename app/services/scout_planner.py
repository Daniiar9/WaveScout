from __future__ import annotations

import json

from app.adapters.manual_discovery import ManualDiscovery
from app.adapters.search_discovery_placeholder import SearchDiscoveryPlaceholder
from app.adapters.tiktok_research_discovery_placeholder import TikTokResearchDiscoveryPlaceholder
from app.models import CreatorContentSample, ScoutRunPlan
from app.models.creator_search_strategy import CreatorSearchStrategy
from app.models.owned_tiktok_profile import OwnedTikTokProfile
from app.models.product_intelligence import ProductIntelligenceBrief, TrendWaveMap
from app.models.common import to_plain_dict
from app.services.creator_search_strategy import build_creator_search_strategy, render_search_strategy_markdown
from app.services.owned_tiktok_analysis import (
    analyze_owned_tiktok_profile,
    identify_content_gaps,
    identify_creator_collab_opportunities,
    render_owned_tiktok_profile_markdown,
)
from app.services.product_intelligence import (
    build_product_intelligence_from_text,
    build_product_intelligence_from_url,
    render_product_brief_markdown,
)
from app.services.text import stable_id
from app.services.trend_wave_mapper import build_trend_wave_map, render_trend_wave_map_markdown


def build_scout_run_plan(
    product_url: str | None = None,
    product_text: str | None = None,
    owned_tiktok_handle: str | None = None,
    owned_content: list[CreatorContentSample] | None = None,
    owned_comments: list[str | dict] | None = None,
    allow_fetch: bool = False,
) -> ScoutRunPlan:
    if product_text:
        product_brief = build_product_intelligence_from_text(product_text, product_url)
        product_fetch = False
    else:
        product_brief = build_product_intelligence_from_url(product_url or "", allow_fetch=allow_fetch)
        product_fetch = False
    wave_map = build_trend_wave_map(product_brief)
    owned_profile = None
    if owned_tiktok_handle:
        owned_profile = analyze_owned_tiktok_profile(owned_tiktok_handle, owned_content, owned_comments)
        owned_profile.content_gaps = identify_content_gaps(product_brief, owned_profile)
        owned_profile.creator_collab_opportunities = identify_creator_collab_opportunities(product_brief, owned_profile)
    strategy = build_creator_search_strategy(product_brief, wave_map, owned_profile)
    adapter_status = _adapter_status()
    dry_queries = _dry_run_queries(strategy)
    safety_status = {
        "external_calls": False,
        "product_fetch": product_fetch,
        "tiktok_live_calls": False,
        "tiktok_scraping": False,
        "tiktok_dm_send": False,
        "message_sending": False,
        "dry_run": True,
    }
    return ScoutRunPlan(
        id=stable_id("scout_plan", product_brief.id, owned_tiktok_handle or ""),
        product_brief=product_brief,
        wave_map=wave_map,
        owned_tiktok_profile_optional=owned_profile,
        search_strategy=strategy,
        discovery_adapters=adapter_status,
        dry_run_queries=dry_queries,
        expected_inputs=[
            "product text or approved product URL fetch",
            "manual creator CSV/JSON imports",
            "optional owned TikTok content/comment imports",
        ],
        expected_outputs=[
            "creator search strategy",
            "dry-run discovery payloads",
            "creator candidates for manual review",
            "creator intelligence packets after candidate import",
        ],
        safety_status=safety_status,
        next_safe_actions=[
            "Review the scout plan and reject criteria.",
            "Run discovery dry-run and inspect generated query payloads.",
            "Use manual import or approved future providers to collect candidate creators.",
            "Build Creator Intelligence Packets for shortlisted candidates.",
            "Human-review any outreach draft before manual contact.",
        ],
    )


def run_discovery_dry_run(scout_run_plan: ScoutRunPlan, limit: int = 25) -> list[dict]:
    adapters = [
        ManualDiscovery(),
        SearchDiscoveryPlaceholder(),
        TikTokResearchDiscoveryPlaceholder(),
    ]
    results = [
        adapter.discover_candidates(scout_run_plan.search_strategy, limit=limit, live=False)
        for adapter in adapters
    ]
    return [to_plain_dict(result) for result in results]


def render_scout_run_plan_markdown(plan: ScoutRunPlan) -> str:
    owned = (
        render_owned_tiktok_profile_markdown(plan.owned_tiktok_profile_optional)
        if plan.owned_tiktok_profile_optional
        else "# Owned TikTok Account Intelligence\n\nNo owned TikTok profile provided or imported.\n"
    )
    return f"""# WaveScout Product-Led Scout Plan

{render_product_brief_markdown(plan.product_brief)}

{render_trend_wave_map_markdown(plan.wave_map)}

{owned}

{render_search_strategy_markdown(plan.search_strategy)}

## Discovery Queries
{render_discovery_queries_markdown(plan)}

## Discovery Adapter Status
{_adapter_table(plan.discovery_adapters)}

## Expected Inputs
{_bullets(plan.expected_inputs)}

## Expected Outputs
{_bullets(plan.expected_outputs)}

## Safety Status
{_safety_lines(plan.safety_status)}

## Next Safe Actions
{_bullets(plan.next_safe_actions)}
"""


def render_discovery_queries_markdown(plan: ScoutRunPlan) -> str:
    if not plan.dry_run_queries:
        return "- None."
    return "\n".join(
        f"- `{payload['adapter']}` would search `{payload['query']}` with limit {payload['limit']}"
        for payload in plan.dry_run_queries
    )


def render_scout_plan_json(plan: ScoutRunPlan) -> str:
    return json.dumps(to_plain_dict(plan), indent=2, sort_keys=True)


def scout_plan_from_dict(payload: dict) -> ScoutRunPlan:
    owned_payload = payload.get("owned_tiktok_profile_optional")
    return ScoutRunPlan(
        id=payload["id"],
        product_brief=ProductIntelligenceBrief(**payload["product_brief"]),
        wave_map=TrendWaveMap(**payload["wave_map"]),
        search_strategy=CreatorSearchStrategy(**payload["search_strategy"]),
        owned_tiktok_profile_optional=OwnedTikTokProfile(**owned_payload) if owned_payload else None,
        discovery_adapters=payload.get("discovery_adapters", []),
        dry_run_queries=payload.get("dry_run_queries", []),
        expected_inputs=payload.get("expected_inputs", []),
        expected_outputs=payload.get("expected_outputs", []),
        safety_status=payload.get("safety_status", {}),
        next_safe_actions=payload.get("next_safe_actions", []),
    )


def _adapter_status() -> list[dict]:
    return [
        {
            "name": "manual_import",
            "supports_live": False,
            "requires_external_calls": False,
            "status": "available",
            "reason": "Uses human-provided imported creator data.",
        },
        {
            "name": "search_provider_placeholder",
            "supports_live": False,
            "requires_external_calls": True,
            "status": "dry_run_only",
            "reason": "No external search provider connected.",
        },
        {
            "name": "official_tiktok_research_placeholder",
            "supports_live": False,
            "requires_external_calls": True,
            "status": "dry_run_only_or_blocked",
            "reason": "Uses capability checker; no live TikTok calls in this pass.",
        },
    ]


def _dry_run_queries(strategy) -> list[dict]:
    payloads = []
    for query in strategy.search_queries[:12]:
        payloads.append(
            {
                "adapter": "search_provider_placeholder",
                "query": query,
                "hashtags": strategy.hashtags[:8],
                "limit": 25,
                "external_calls": False,
            }
        )
    for keyword in strategy.keywords[:8]:
        payloads.append(
            {
                "adapter": "official_tiktok_research_placeholder",
                "query": keyword,
                "hashtags": strategy.hashtags[:8],
                "limit": 25,
                "external_calls": False,
            }
        )
    return payloads


def _adapter_table(adapters: list[dict]) -> str:
    rows = ["| Adapter | Status | External Calls Required | Reason |", "|---|---|---|---|"]
    for adapter in adapters:
        rows.append(
            f"| {adapter['name']} | {adapter['status']} | {str(adapter['requires_external_calls']).lower()} | {adapter['reason']} |"
        )
    return "\n".join(rows)


def _safety_lines(status: dict) -> str:
    return "\n".join(f"- {key}={str(value).lower()}" for key, value in status.items())


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)
