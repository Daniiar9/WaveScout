from __future__ import annotations

from app.config import AppConfig, load_config
from app.models.common import to_plain_dict
from app.services.tiktok_capability_service import require_capability


def query_videos_dry_run(query: dict, fields: list[str] | None = None, config: AppConfig | None = None) -> dict:
    config = config or load_config()
    gate = require_capability("research_query_videos", config)
    return {
        "capability": "research_query_videos",
        "dry_run": True,
        "external_calls_made": False,
        "live_mode_allowed": False,
        "human_approval_required": True,
        "gate": to_plain_dict(gate),
        "request_preview": {
            "endpoint": "/v2/research/video/query/",
            "query": query,
            "fields": fields or ["id", "username", "video_description", "create_time"],
        },
    }


def query_comments_dry_run(video_id: str, config: AppConfig | None = None) -> dict:
    config = config or load_config()
    gate = require_capability("research_query_comments", config)
    return {
        "capability": "research_query_comments",
        "dry_run": True,
        "external_calls_made": False,
        "live_mode_allowed": False,
        "human_approval_required": True,
        "gate": to_plain_dict(gate),
        "request_preview": {
            "endpoint": "official research comments endpoint placeholder",
            "video_id": video_id,
            "fields": ["id", "text", "like_count", "create_time"],
        },
    }


def query_videos_live(query: dict, fields: list[str] | None = None, config: AppConfig | None = None) -> dict:
    gate = require_capability("research_query_videos", config or load_config())
    raise NotImplementedError(gate.reason)

