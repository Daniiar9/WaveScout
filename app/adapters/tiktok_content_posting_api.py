from __future__ import annotations

from app.config import AppConfig, load_config
from app.models.common import to_plain_dict
from app.services.tiktok_capability_service import require_capability

POSTING_BLOCKED_REASON = "WaveScout does not post content or automate publishing in this pass."


def query_creator_info_dry_run(config: AppConfig | None = None) -> dict:
    config = config or load_config()
    gate = require_capability("content_direct_post", config)
    return {
        "capability": "content_direct_post",
        "operation": "query_creator_info",
        "dry_run": True,
        "external_calls_made": False,
        "live_post": False,
        "live_post_allowed": False,
        "content_posting_supported": False,
        "blocked_reason": POSTING_BLOCKED_REASON,
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
        "live_post": False,
        "live_post_allowed": False,
        "content_posting_supported": False,
        "blocked_reason": POSTING_BLOCKED_REASON,
        "send_allowed": False,
        "human_approval_required": True,
        "gate": to_plain_dict(gate),
        "payload_preview": payload,
        "message": POSTING_BLOCKED_REASON,
    }


def direct_post_video_live(payload: dict, config: AppConfig | None = None) -> dict:
    gate = require_capability("content_direct_post", config or load_config())
    raise NotImplementedError(gate.reason)
