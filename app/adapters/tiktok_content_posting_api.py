from __future__ import annotations

from app.config import AppConfig, load_config
from app.models.common import to_plain_dict
from app.services.tiktok_capability_service import require_capability


def query_creator_info_dry_run(config: AppConfig | None = None) -> dict:
    config = config or load_config()
    gate = require_capability("content_direct_post", config)
    return {
        "capability": "content_direct_post",
        "operation": "query_creator_info",
        "dry_run": True,
        "external_calls_made": False,
        "live_post_allowed": False,
        "human_approval_required": True,
        "gate": to_plain_dict(gate),
        "request_preview": {"endpoint": "official creator info endpoint placeholder"},
    }


def direct_post_video_dry_run(payload: dict, config: AppConfig | None = None) -> dict:
    config = config or load_config()
    gate = require_capability("content_direct_post", config)
    return {
        "capability": "content_direct_post",
        "operation": "direct_post_video",
        "dry_run": True,
        "external_calls_made": False,
        "live_post_allowed": False,
        "send_allowed": False,
        "human_approval_required": True,
        "gate": to_plain_dict(gate),
        "payload_preview": payload,
        "message": "Dry-run only. No video is posted by WaveScout.",
    }


def direct_post_video_live(payload: dict, config: AppConfig | None = None) -> dict:
    gate = require_capability("content_direct_post", config or load_config())
    raise NotImplementedError(gate.reason)

