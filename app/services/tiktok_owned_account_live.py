from __future__ import annotations

from app.config import AppConfig, load_config
from app.models import CreatorContentSample, OwnedTikTokProfile
from app.models.common import to_plain_dict
from app.services.live_discovery_gate import default_live_safety_status
from app.services.owned_tiktok_analysis import analyze_owned_tiktok_profile, render_owned_tiktok_profile_markdown
from app.services.tiktok_capability_service import parse_approved_scopes
from app.services.text import normalize_handle, stable_id

REQUIRED_DISPLAY_SCOPES = ["user.info.basic", "video.list"]


def check_tiktok_owned_account_live(
    config: AppConfig | None = None,
    allow_tiktok_live: bool = False,
    dry_run: bool = True,
    handle: str = "@owned_account",
) -> dict:
    config = config or load_config()
    configured_scopes = _configured_scopes(config)
    missing_scopes = [scope for scope in REQUIRED_DISPLAY_SCOPES if scope not in configured_scopes]
    blocked_reason = _display_blocked_reason(config, allow_tiktok_live, dry_run, missing_scopes)
    blocked = bool(blocked_reason)
    profile = analyze_owned_tiktok_profile(handle)
    return {
        "provider": "tiktok_display_api",
        "dry_run": True,
        "blocked": blocked,
        "blocked_reason": blocked_reason,
        "required_scopes": REQUIRED_DISPLAY_SCOPES,
        "missing_scopes": missing_scopes,
        "has_access_token": bool(config.tiktok_access_token),
        "external_calls": False,
        "tiktok_live_calls": False,
        "content_posting_supported": False,
        "owned_tiktok_profile": to_plain_dict(profile),
        "request_previews": [
            {"endpoint": "/v2/user/info/", "fields": ["open_id", "union_id", "avatar_url", "display_name"]},
            {"endpoint": "/v2/video/list/", "fields": ["id", "title", "share_url", "cover_image_url"]},
        ],
        "safety_status": default_live_safety_status(dry_run=True, external_calls=False, tiktok_live_calls=False),
    }


def owned_profile_from_display_response(user_info: dict, videos: list[dict]) -> OwnedTikTokProfile:
    handle = normalize_handle(user_info.get("display_name") or user_info.get("username") or "@owned_account")
    samples = [
        CreatorContentSample(
            id=stable_id("owned_video", video.get("id", ""), video.get("title", "")),
            creator_id=handle,
            title_or_caption=str(video.get("title") or video.get("description") or ""),
            transcript_or_summary=str(video.get("title") or video.get("description") or ""),
            video_url=str(video.get("share_url") or ""),
            topics=[],
            format="owned_video",
        )
        for video in videos
    ]
    return analyze_owned_tiktok_profile(handle, content_samples=samples)


def render_tiktok_owned_account_live_markdown(status: dict) -> str:
    profile = status.get("owned_tiktok_profile", {})
    profile_markdown = (
        render_owned_tiktok_profile_markdown(OwnedTikTokProfile(**profile))
        if isinstance(profile, dict) and profile.get("handle")
        else "No owned profile built."
    )
    return f"""# TikTok Owned Account Live Gate

- Dry run: {str(status.get("dry_run", True)).lower()}
- Blocked: {str(status.get("blocked", True)).lower()}
- Blocked reason: {status.get("blocked_reason", "")}
- External calls: false
- TikTok live calls: false

## Required Scopes

{_bullets(status.get("required_scopes", []))}

## Missing Scopes

{_bullets(status.get("missing_scopes", []))}

## Owned Account Analysis

{profile_markdown}
"""


def _display_blocked_reason(
    config: AppConfig,
    allow_tiktok_live: bool,
    dry_run: bool,
    missing_scopes: list[str],
) -> str:
    if dry_run:
        return "Dry-run only; no TikTok Display API call was attempted."
    if not allow_tiktok_live:
        return "Blocked because explicit --allow-tiktok-live was not provided."
    if not config.wavescout_allow_tiktok_live:
        return "Blocked because WAVESCOUT_ALLOW_TIKTOK_LIVE=false."
    if not config.tiktok_access_token:
        return "Blocked because TIKTOK_ACCESS_TOKEN is not configured."
    if missing_scopes:
        return f"Blocked because required scopes are missing: {', '.join(missing_scopes)}."
    return "Live Display API integration pending audited HTTP implementation."


def _configured_scopes(config: AppConfig) -> list[str]:
    return parse_approved_scopes(",".join([config.tiktok_scopes, config.tiktok_approved_scopes]))


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)
