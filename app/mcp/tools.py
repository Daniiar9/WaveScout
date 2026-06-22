from __future__ import annotations

from typing import Callable

from app.config import DEFAULT_PRODUCT_CONTEXT, load_config
from app.adapters.tiktok_content_posting_api import direct_post_video_dry_run
from app.adapters.tiktok_display_api import get_user_info_dry_run
from app.adapters.tiktok_research_api import query_videos_dry_run as research_query_videos_dry_run
from app.models.common import to_plain_dict
from app.services import creator_discovery
from app.services import trend_wave_service
from app.services import creator_scoring as scoring_service
from app.services.audience_analysis import infer_audience_profile as infer_audience_profile_service
from app.services.comment_intelligence import extract_comment_signals, summarize_comment_intelligence
from app.services.content_angle_generator import generate_content_angles as generate_angles_service
from app.services.creator_content_analysis import summarize_creator_content
from app.services.notion_sync import sync_creator_to_notion as sync_creator_packet_service
from app.services.notion_sync import sync_outreach_packet_to_notion as sync_outreach_service
from app.services.outreach_packet_builder import (
    build_creator_intelligence_packet as build_packet_service,
)
from app.services.outreach_packet_builder import build_outreach_packet as build_outreach_service
from app.services.outreach_packet_builder import creator_packet_contract
from app.services.proposal_generator import generate_creator_proposal as generate_proposal_service
from app.services.product_intelligence import build_product_intelligence_from_text, build_product_intelligence_from_url
from app.services.trend_wave_mapper import build_trend_wave_map as build_trend_wave_map_service
from app.services.creator_search_strategy import build_creator_search_strategy as build_creator_search_strategy_service
from app.services.owned_tiktok_analysis import analyze_owned_tiktok_profile
from app.services.scout_planner import (
    build_scout_run_plan as build_scout_run_plan_service,
    run_discovery_dry_run as run_discovery_dry_run_service,
)
from app.services.storage import LocalJSONStorage
from app.services.tiktok_capability_service import (
    build_oauth_setup_instructions,
    build_tiktok_capability_report,
    check_capability as check_tiktok_capability_service,
    parse_approved_scopes,
)


def list_trend_waves() -> dict:
    waves = trend_wave_service.list_trend_waves()
    return {"offline": True, "trend_waves": to_plain_dict(waves)}


def create_trend_wave(payload: dict) -> dict:
    wave = trend_wave_service.create_trend_wave(payload)
    return {"offline": True, "trend_wave": to_plain_dict(wave)}


def import_creator_candidate(payload: dict) -> dict:
    creator = creator_discovery.import_creator_candidate(payload)
    return {"offline": True, "creator": to_plain_dict(creator)}


def import_creator_content_sample(payload: dict) -> dict:
    sample = creator_discovery.import_creator_content_sample(payload)
    return {"offline": True, "content_sample": to_plain_dict(sample)}


def import_comment_samples(creator_id: str, comments: list[str], video_url: str = "", content_id: str | None = None) -> dict:
    imported = creator_discovery.import_comment_samples(creator_id, comments, video_url, content_id)
    return {"offline": True, "comments": imported}


def score_creator_for_wave(
    creator_handle: str,
    wave: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
) -> dict:
    storage = LocalJSONStorage()
    creator, trend_wave, content, raw_comments = _load_context(storage, creator_handle, wave)
    signals = extract_comment_signals(raw_comments, creator.id)
    content_summary = summarize_creator_content(creator, content)
    audience = infer_audience_profile_service(creator, content, signals, product_context)
    score = scoring_service.score_creator_for_wave(
        creator, trend_wave, content, signals, product_context, audience, content_summary
    )
    return {"offline": True, "send_allowed": False, "score": to_plain_dict(score)}


def analyze_creator_comments(creator_handle: str) -> dict:
    storage = LocalJSONStorage()
    creator = _require_creator(storage, creator_handle)
    signals = extract_comment_signals(storage.comments_for_creator(creator.id), creator.id)
    return {
        "offline": True,
        "creator": creator.handle,
        "signals": to_plain_dict(signals),
        "summary": summarize_comment_intelligence(signals),
    }


def infer_creator_audience(
    creator_handle: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
) -> dict:
    storage = LocalJSONStorage()
    creator = _require_creator(storage, creator_handle)
    content = storage.content_for_creator(creator.id)
    signals = extract_comment_signals(storage.comments_for_creator(creator.id), creator.id)
    profile = infer_audience_profile_service(creator, content, signals, product_context)
    return {"offline": True, "audience_profile": to_plain_dict(profile)}


def generate_content_angles(
    creator_handle: str,
    wave: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
) -> dict:
    storage = LocalJSONStorage()
    creator, trend_wave, content, raw_comments = _load_context(storage, creator_handle, wave)
    signals = extract_comment_signals(raw_comments, creator.id)
    content_summary = summarize_creator_content(creator, content)
    audience = infer_audience_profile_service(creator, content, signals, product_context)
    comment_summary = summarize_comment_intelligence(signals)
    angles = generate_angles_service(product_context, trend_wave, creator, content_summary, audience, comment_summary)
    return {"offline": True, "send_allowed": False, "angles": to_plain_dict(angles)}


def generate_creator_proposal(
    creator_handle: str,
    wave: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
) -> dict:
    storage = LocalJSONStorage()
    packet = _build_packet_from_storage(storage, creator_handle, wave, product_context)
    return {"offline": True, "send_allowed": False, "proposal": to_plain_dict(packet.proposal_draft)}


def build_creator_intelligence_packet(
    creator_handle: str,
    wave: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
) -> dict:
    storage = LocalJSONStorage()
    packet = _build_packet_from_storage(storage, creator_handle, wave, product_context)
    return {
        "offline": True,
        "send_allowed": False,
        "packet": to_plain_dict(packet),
        "packet_contract": creator_packet_contract(packet),
    }


def build_outreach_packet(
    creator_handle: str,
    wave: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
) -> dict:
    storage = LocalJSONStorage()
    packet = _build_packet_from_storage(storage, creator_handle, wave, product_context)
    outreach = build_outreach_service(packet)
    return {"offline": True, "send_allowed": False, "outreach_packet": to_plain_dict(outreach)}


def sync_creator_to_notion(
    creator_handle: str,
    wave: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
) -> dict:
    storage = LocalJSONStorage()
    packet = _build_packet_from_storage(storage, creator_handle, wave, product_context)
    result = sync_creator_packet_service(packet, load_config())
    return {"offline": True, "send_allowed": False, "notion_sync": to_plain_dict(result)}


def sync_outreach_packet_to_notion(
    creator_handle: str,
    wave: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
) -> dict:
    storage = LocalJSONStorage()
    packet = _build_packet_from_storage(storage, creator_handle, wave, product_context)
    outreach = build_outreach_service(packet)
    result = sync_outreach_service(outreach, load_config())
    return {"offline": True, "send_allowed": False, "notion_sync": to_plain_dict(result)}


def run_wave_scout(
    wave: str,
    product_context: str = DEFAULT_PRODUCT_CONTEXT,
    top: int = 3,
) -> dict:
    storage = LocalJSONStorage()
    trend_wave = _require_wave(storage, wave)
    packets = [
        build_packet_service(
            product_context,
            trend_wave,
            creator,
            storage.content_for_creator(creator.id),
            storage.comments_for_creator(creator.id),
        )
        for creator in storage.load_creators()
    ]
    ranked = sorted(packets, key=lambda packet: packet.fit_score.score, reverse=True)
    return {
        "offline": True,
        "external_calls_made": False,
        "send_allowed": False,
        "top_packets": to_plain_dict(ranked[:top]),
        "rejected": [
            packet.creator_candidate.handle
            for packet in ranked
            if packet.fit_score.fit_level == "reject"
        ],
    }


def check_tiktok_capabilities() -> dict:
    report = build_tiktok_capability_report(load_config())
    return {
        "offline": True,
        "external_calls_made": False,
        "tiktok_scraping": False,
        "tiktok_dm_send": False,
        "report": to_plain_dict(report),
    }


def get_tiktok_capability(name: str) -> dict:
    capability = check_tiktok_capability_service(name, load_config())
    return {
        "offline": True,
        "external_calls_made": False,
        "capability": to_plain_dict(capability),
    }


def build_tiktok_oauth_setup_instructions(requested_scopes: str | list[str] = "user.info.basic,video.list") -> dict:
    scopes = parse_approved_scopes(requested_scopes) if isinstance(requested_scopes, str) else requested_scopes
    return build_oauth_setup_instructions(scopes)


def tiktok_display_user_info_dry_run() -> dict:
    return get_user_info_dry_run(load_config())


def tiktok_research_query_dry_run(query: dict | None = None, fields: list[str] | None = None) -> dict:
    return research_query_videos_dry_run(query or {}, fields, load_config())


def tiktok_content_post_dry_run(payload: dict | None = None) -> dict:
    result = direct_post_video_dry_run(payload or {}, load_config())
    result["live_post_allowed"] = False
    result["human_approval_required"] = True
    return result


def build_product_intelligence_brief(
    product_text: str = "",
    product_url: str = "",
    allow_fetch: bool = False,
) -> dict:
    brief = (
        build_product_intelligence_from_text(product_text, product_url or None)
        if product_text
        else build_product_intelligence_from_url(product_url, allow_fetch=allow_fetch)
    )
    return {"offline": True, "external_calls_made": False, "safety_status": _planner_safety(), "product_brief": to_plain_dict(brief)}


def build_trend_wave_map(product_text: str, product_url: str = "") -> dict:
    brief = build_product_intelligence_from_text(product_text, product_url or None)
    wave_map = build_trend_wave_map_service(brief)
    return {"offline": True, "external_calls_made": False, "safety_status": _planner_safety(), "wave_map": to_plain_dict(wave_map)}


def build_creator_search_strategy(product_text: str, product_url: str = "") -> dict:
    brief = build_product_intelligence_from_text(product_text, product_url or None)
    wave_map = build_trend_wave_map_service(brief)
    strategy = build_creator_search_strategy_service(brief, wave_map)
    return {"offline": True, "external_calls_made": False, "safety_status": _planner_safety(), "search_strategy": to_plain_dict(strategy)}


def analyze_owned_tiktok_profile_dry_run(handle: str, comments: list[str] | None = None) -> dict:
    profile = analyze_owned_tiktok_profile(handle, comments=comments or [])
    return {"offline": True, "external_calls_made": False, "safety_status": _planner_safety(), "owned_tiktok_profile": to_plain_dict(profile)}


def build_scout_run_plan(
    product_text: str = "",
    product_url: str = "",
    owned_tiktok_handle: str = "",
    allow_fetch: bool = False,
) -> dict:
    plan = build_scout_run_plan_service(
        product_url=product_url or None,
        product_text=product_text or None,
        owned_tiktok_handle=owned_tiktok_handle or None,
        allow_fetch=allow_fetch,
    )
    return {"offline": True, "external_calls_made": False, "safety_status": plan.safety_status, "scout_run_plan": to_plain_dict(plan)}


def run_discovery_dry_run(product_text: str = DEFAULT_PRODUCT_CONTEXT, limit: int = 25) -> dict:
    plan = build_scout_run_plan_service(product_text=product_text)
    results = run_discovery_dry_run_service(plan, limit=limit)
    return {"offline": True, "external_calls_made": False, "safety_status": plan.safety_status, "discovery_results": results}


TOOL_REGISTRY: dict[str, Callable] = {
    "list_trend_waves": list_trend_waves,
    "create_trend_wave": create_trend_wave,
    "import_creator_candidate": import_creator_candidate,
    "import_creator_content_sample": import_creator_content_sample,
    "import_comment_samples": import_comment_samples,
    "score_creator_for_wave": score_creator_for_wave,
    "analyze_creator_comments": analyze_creator_comments,
    "infer_creator_audience": infer_creator_audience,
    "generate_content_angles": generate_content_angles,
    "generate_creator_proposal": generate_creator_proposal,
    "build_creator_intelligence_packet": build_creator_intelligence_packet,
    "build_outreach_packet": build_outreach_packet,
    "sync_creator_to_notion": sync_creator_to_notion,
    "sync_outreach_packet_to_notion": sync_outreach_packet_to_notion,
    "run_wave_scout": run_wave_scout,
    "check_tiktok_capabilities": check_tiktok_capabilities,
    "get_tiktok_capability": get_tiktok_capability,
    "build_tiktok_oauth_setup_instructions": build_tiktok_oauth_setup_instructions,
    "tiktok_display_user_info_dry_run": tiktok_display_user_info_dry_run,
    "tiktok_research_query_dry_run": tiktok_research_query_dry_run,
    "tiktok_content_post_dry_run": tiktok_content_post_dry_run,
    "build_product_intelligence_brief": build_product_intelligence_brief,
    "build_trend_wave_map": build_trend_wave_map,
    "build_creator_search_strategy": build_creator_search_strategy,
    "analyze_owned_tiktok_profile_dry_run": analyze_owned_tiktok_profile_dry_run,
    "build_scout_run_plan": build_scout_run_plan,
    "run_discovery_dry_run": run_discovery_dry_run,
}


def register_tools(server: object) -> object:
    for name, func in TOOL_REGISTRY.items():
        server.tool(name=name)(func)
    return server


def _build_packet_from_storage(
    storage: LocalJSONStorage,
    creator_handle: str,
    wave: str,
    product_context: str,
):
    creator, trend_wave, content, comments = _load_context(storage, creator_handle, wave)
    return build_packet_service(product_context, trend_wave, creator, content, comments)


def _load_context(storage: LocalJSONStorage, creator_handle: str, wave: str):
    creator = _require_creator(storage, creator_handle)
    trend_wave = _require_wave(storage, wave)
    content = storage.content_for_creator(creator.id)
    comments = storage.comments_for_creator(creator.id)
    return creator, trend_wave, content, comments


def _require_creator(storage: LocalJSONStorage, creator_handle: str):
    creator = storage.find_creator(creator_handle)
    if not creator:
        raise ValueError(f"Creator not found in local data: {creator_handle}")
    return creator


def _require_wave(storage: LocalJSONStorage, wave: str):
    trend_wave = storage.find_wave(wave)
    if not trend_wave:
        raise ValueError(f"Trend wave not found in local data: {wave}")
    return trend_wave


def _planner_safety() -> dict:
    return {
        "external_calls": False,
        "product_fetch": False,
        "tiktok_live_calls": False,
        "tiktok_scraping": False,
        "tiktok_dm_send": False,
        "message_sending": False,
    }
