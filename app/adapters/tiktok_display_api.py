from __future__ import annotations

from app.config import AppConfig, load_config
from app.models.common import to_plain_dict
from app.services.tiktok_capability_service import require_capability


def get_user_info_dry_run(config: AppConfig | None = None) -> dict:
    config = config or load_config()
    gate = require_capability("display_user_info", config)
    return _dry_run_response(
        "display_user_info",
        gate,
        {"endpoint": "/v2/user/info/", "fields": ["open_id", "union_id", "avatar_url", "display_name"]},
    )


def list_videos_dry_run(config: AppConfig | None = None) -> dict:
    config = config or load_config()
    gate = require_capability("display_list_videos", config)
    return _dry_run_response(
        "display_list_videos",
        gate,
        {"endpoint": "/v2/video/list/", "fields": ["id", "title", "cover_image_url", "share_url"]},
    )


def query_videos_dry_run(video_ids: list[str], config: AppConfig | None = None) -> dict:
    config = config or load_config()
    gate = require_capability("display_query_videos", config)
    return _dry_run_response(
        "display_query_videos",
        gate,
        {"endpoint": "/v2/video/query/", "video_ids": video_ids, "fields": ["id", "title", "share_url"]},
    )


def get_user_info_live(config: AppConfig | None = None) -> dict:
    gate = require_capability("display_user_info", config or load_config())
    raise NotImplementedError(gate.reason)


def _dry_run_response(capability: str, gate, request_preview: dict) -> dict:
    return {
        "capability": capability,
        "dry_run": True,
        "external_calls_made": False,
        "live_mode_allowed": False,
        "human_approval_required": True,
        "gate": to_plain_dict(gate),
        "request_preview": request_preview,
    }

