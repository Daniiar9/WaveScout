from __future__ import annotations

from app.config import AppConfig, load_config
from app.services.live_discovery_gate import default_live_safety_status
from app.services.tiktok_capability_service import check_capability, parse_approved_scopes

REQUIRED_RESEARCH_SCOPES = ["research.data.basic"]


def check_tiktok_research_live(
    query: str = "AI workflow automation",
    config: AppConfig | None = None,
    allow_tiktok_live: bool = False,
    dry_run: bool = True,
) -> dict:
    config = config or load_config()
    configured_scopes = parse_approved_scopes(",".join([config.tiktok_scopes, config.tiktok_approved_scopes]))
    missing_scopes = [scope for scope in REQUIRED_RESEARCH_SCOPES if scope not in configured_scopes]
    video_capability = check_capability("research_query_videos", config)
    comments_capability = check_capability("research_query_comments", config)
    blocked_reason = _research_blocked_reason(config, allow_tiktok_live, dry_run, missing_scopes)
    return {
        "provider": "tiktok_research_api",
        "dry_run": True,
        "blocked": True,
        "blocked_reason": blocked_reason,
        "query": query,
        "required_scopes": REQUIRED_RESEARCH_SCOPES,
        "missing_scopes": missing_scopes,
        "video_capability_status": video_capability.status,
        "comments_capability_status": comments_capability.status,
        "external_calls": False,
        "tiktok_live_calls": False,
        "raw_results": [],
        "normalized_candidates": [],
        "request_payloads": [
            {
                "endpoint": "/v2/research/video/query/",
                "query": {"keyword": query},
                "fields": ["id", "username", "video_description", "create_time"],
                "external_calls": False,
            },
            {
                "endpoint": "official research comments endpoint placeholder",
                "query": {"keyword": query},
                "requires_capability": "research_query_comments",
                "external_calls": False,
            },
        ],
        "safe_next_actions": [
            "Confirm Research API approval in the TikTok developer portal.",
            "Configure scopes locally only after approval.",
            "Keep manual review between discovery and outreach.",
        ],
        "safety_status": default_live_safety_status(dry_run=True, external_calls=False, tiktok_live_calls=False),
    }


def render_tiktok_research_live_markdown(status: dict) -> str:
    return f"""# TikTok Research Live Gate

- Dry run: {str(status.get("dry_run", True)).lower()}
- Blocked: {str(status.get("blocked", True)).lower()}
- Blocked reason: {status.get("blocked_reason", "")}
- Query: {status.get("query", "")}
- External calls: false
- TikTok live calls: false

## Required Scopes

{_bullets(status.get("required_scopes", []))}

## Missing Scopes

{_bullets(status.get("missing_scopes", []))}

## Safe Next Actions

{_bullets(status.get("safe_next_actions", []))}
"""


def _research_blocked_reason(
    config: AppConfig,
    allow_tiktok_live: bool,
    dry_run: bool,
    missing_scopes: list[str],
) -> str:
    if dry_run:
        return "Dry-run only; no TikTok Research API call was attempted."
    if not allow_tiktok_live:
        return "Blocked because explicit --allow-tiktok-live was not provided."
    if not config.wavescout_allow_tiktok_live:
        return "Blocked because WAVESCOUT_ALLOW_TIKTOK_LIVE=false."
    if not config.tiktok_research_api_enabled:
        return "Blocked because TIKTOK_RESEARCH_API_ENABLED=false and research approval is not configured."
    if not config.tiktok_access_token:
        return "Blocked because TIKTOK_ACCESS_TOKEN is not configured."
    if missing_scopes:
        return f"Blocked because required scopes are missing: {', '.join(missing_scopes)}."
    return "Live Research API integration pending capability approval and audited HTTP implementation."


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)
