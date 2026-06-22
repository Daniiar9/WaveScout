from __future__ import annotations

import json
from pathlib import Path

from app.models import (
    CreatorCandidate,
    CreatorContentSample,
    DiscoveryCandidateNormalized,
    GrowthBrief,
)
from app.models.common import to_plain_dict
from app.services.discovery_candidate_normalizer import normalize_discovery_candidate
from app.services.discovery_dedupe import dedupe_discovery_candidates, rank_discovery_candidates_initial
from app.services.discovery_provider_service import list_discovery_providers, run_discovery_provider_dry_run
from app.services.notion_pipeline_builder import build_notion_pipeline_payloads
from app.services.outreach_packet_builder import build_creator_intelligence_packet
from app.services.scout_planner import build_scout_run_plan
from app.services.storage import LocalJSONStorage, coerce_dataclass
from app.services.text import normalize_handle, stable_id


def run_growth_engine(
    product_url: str | None = None,
    product_text: str | None = None,
    owned_tiktok: str | None = None,
    owned_content: list[CreatorContentSample] | None = None,
    owned_comments: list[str | dict] | None = None,
    imported_creators: str | list[CreatorCandidate] | None = None,
    imported_content: str | list[CreatorContentSample] | None = None,
    imported_comments: str | list[dict] | None = None,
    discovery_limit: int = 25,
    top_creators: int = 5,
    dry_run: bool = True,
    allow_fetch: bool = False,
    allow_external_discovery: bool = False,
) -> GrowthBrief:
    if not product_text and not product_url:
        raise ValueError("Product input is required. Provide product_text or product_url.")
    scout_plan = build_scout_run_plan(
        product_url=product_url,
        product_text=product_text,
        owned_tiktok_handle=owned_tiktok,
        owned_content=owned_content,
        owned_comments=owned_comments,
        allow_fetch=allow_fetch,
    )
    providers = list_discovery_providers()
    run_results = [
        run_discovery_provider_dry_run(provider, scout_plan.search_strategy, discovery_limit, scout_plan.id)
        for provider in providers
    ]
    raw_candidates = []
    imported_creators_requested = imported_creators is not None
    for result in run_results:
        if result.provider.provider_type == "manual_import" and not imported_creators_requested:
            continue
        raw_candidates.extend(result.candidates)
    creators = _load_creators(imported_creators)
    content_samples = _load_content(imported_content)
    comments = _load_comments(imported_comments)
    raw_candidates.extend(_candidates_from_imported_creators(creators, scout_plan))
    normalized = [normalize_discovery_candidate(candidate) for candidate in raw_candidates]
    ranked_candidates = rank_discovery_candidates_initial(dedupe_discovery_candidates(normalized), scout_plan.search_strategy)
    packets = _build_packets_for_imported_creators(
        creators,
        content_samples,
        comments,
        scout_plan,
        top_creators,
    )
    safety_status = {
        "external_calls": False,
        "tiktok_scraping": False,
        "tiktok_dm_send": False,
        "browser_automation": False,
        "live_post": False,
        "send_allowed": False,
        "approval_required": True,
        "human_review_required": True,
        "notion_write": False,
        "dry_run": True,
    }
    discovery_summary = {
        "providers_checked": len(providers),
        "dry_run_payloads": sum(len(result.payload.get("dry_run_payloads", [])) for result in run_results),
        "candidates_from_manual_import": len(creators),
        "candidates_needing_enrichment": _candidates_needing_enrichment(creators, content_samples, comments),
        "normalized_candidates": len(ranked_candidates),
        "creator_packets": len(packets),
        "external_calls": False,
    }
    missing_data = _missing_data(creators, content_samples, comments, ranked_candidates)
    growth_brief = GrowthBrief(
        id=stable_id("growth_brief", scout_plan.id, len(ranked_candidates), len(packets)),
        product_brief=scout_plan.product_brief,
        wave_map=scout_plan.wave_map,
        owned_tiktok_profile=scout_plan.owned_tiktok_profile_optional,
        search_strategy=scout_plan.search_strategy,
        discovery_summary=discovery_summary,
        candidate_shortlist=ranked_candidates[: max(top_creators, 10)],
        top_creator_packets=packets,
        content_recommendations=_content_recommendations(scout_plan, packets),
        outreach_recommendations=_outreach_recommendations(packets),
        notion_pipeline_payload={},
        missing_data=missing_data,
        next_safe_actions=_next_safe_actions(packets, ranked_candidates, missing_data),
        safety_status=safety_status,
    )
    growth_brief.notion_pipeline_payload = build_notion_pipeline_payloads(growth_brief, packets)
    return growth_brief


def growth_brief_to_json(growth_brief: GrowthBrief) -> str:
    return json.dumps(to_plain_dict(growth_brief), indent=2, sort_keys=True)


def _load_creators(source: str | list[CreatorCandidate] | None) -> list[CreatorCandidate]:
    if source is None:
        return []
    if isinstance(source, list):
        return source
    path = Path(source)
    if not path.exists():
        return []
    return [coerce_dataclass(CreatorCandidate, item) for item in json.loads(path.read_text(encoding="utf-8"))]


def _load_content(source: str | list[CreatorContentSample] | None) -> list[CreatorContentSample]:
    if source is None:
        return []
    if isinstance(source, list):
        return source
    path = Path(source)
    if not path.exists():
        return []
    return [coerce_dataclass(CreatorContentSample, item) for item in json.loads(path.read_text(encoding="utf-8"))]


def _load_comments(source: str | list[dict] | None) -> list[dict]:
    if source is None:
        return []
    if isinstance(source, list):
        return source
    path = Path(source)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _candidates_from_imported_creators(creators: list[CreatorCandidate], scout_plan) -> list[dict]:
    candidates = []
    for creator in creators:
        candidates.append(
            {
                "handle": creator.handle,
                "display_name": creator.display_name,
                "profile_url": creator.profile_url,
                "bio": creator.bio,
                "matched_query": scout_plan.search_strategy.search_queries[0] if scout_plan.search_strategy.search_queries else "",
                "matched_wave": scout_plan.wave_map.primary_waves[0] if scout_plan.wave_map.primary_waves else "",
                "matched_hashtags": creator.hashtags_used,
                "source_provider": "manual_import",
                "source_confidence": 0.75,
                "reason_found": "Imported creator matched to product-led scout plan.",
                "raw_snippet": creator.bio,
                "requires_manual_review": True,
            }
        )
    return candidates


def _build_packets_for_imported_creators(
    creators: list[CreatorCandidate],
    content_samples: list[CreatorContentSample],
    comments: list[dict],
    scout_plan,
    top_creators: int,
):
    packets = []
    storage = LocalJSONStorage()
    wave = storage.find_wave(scout_plan.wave_map.primary_waves[0]) or storage.load_waves()[0]
    for creator in creators:
        creator_content = [sample for sample in content_samples if sample.creator_id == creator.id]
        creator_comments = [comment for comment in comments if comment.get("creator_id") == creator.id]
        if not creator_content or not creator_comments:
            continue
        packet = build_creator_intelligence_packet(
            scout_plan.product_brief.one_liner,
            wave,
            creator,
            creator_content,
            creator_comments,
        )
        if packet.fit_score.fit_level != "reject":
            packets.append(packet)
    return sorted(packets, key=lambda packet: packet.fit_score.score, reverse=True)[:top_creators]


def _missing_data(
    creators: list[CreatorCandidate],
    content_samples: list[CreatorContentSample],
    comments: list[dict],
    candidates: list[DiscoveryCandidateNormalized],
) -> list[str]:
    missing = []
    if not candidates:
        missing.append("No live creator candidates yet. Connect provider or import creator data.")
    if creators and not content_samples:
        missing.append("Imported creators need content samples before scoring.")
    if creators and not comments:
        missing.append("Imported creators need comment samples for comment intelligence.")
    if not creators:
        missing.append("Manual creator import or approved provider discovery is needed for packets.")
    return missing


def _candidates_needing_enrichment(
    creators: list[CreatorCandidate],
    content_samples: list[CreatorContentSample],
    comments: list[dict],
) -> int:
    if not creators:
        return 0
    content_creator_ids = {sample.creator_id for sample in content_samples}
    comment_creator_ids = {comment.get("creator_id") for comment in comments}
    return sum(
        1
        for creator in creators
        if creator.id not in content_creator_ids or creator.id not in comment_creator_ids
    )


def _content_recommendations(scout_plan, packets) -> list[str]:
    if packets:
        return [packet.recommended_content_angle.title for packet in packets]
    return scout_plan.product_brief.creator_relevant_angles[:5]


def _outreach_recommendations(packets) -> list[str]:
    if not packets:
        return [
            "Do not contact yet. Source and enrich creator candidates first.",
            "Use generated search queries to find creators for manual review.",
        ]
    return [
        f"Review draft for {packet.creator_candidate.handle}: {packet.recommended_content_angle.title}"
        for packet in packets
    ]


def _next_safe_actions(packets, candidates, missing_data: list[str]) -> list[str]:
    actions = []
    if not candidates:
        actions.append("Use generated search queries to source candidates manually or through future approved providers.")
    if missing_data:
        actions.append("Fill missing creator content/comment data before outreach review.")
    if packets:
        actions.append("Review top Creator Intelligence Packets and approve any manual outreach separately.")
    actions.append("Keep send_allowed=false and approval_required=true for every outreach artifact.")
    return actions
