from __future__ import annotations

from dataclasses import dataclass, field

from app.models.common import utc_now_iso


@dataclass
class PerformanceFeedback:
    creator_handle: str
    content_angle: str = ""
    outreach_status: str = ""
    creator_response: str = ""
    post_url: str = ""
    views: int = 0
    likes: int = 0
    comments: int = 0
    clicks: int = 0
    signups: int = 0
    notes: str = ""
    created_at: str = field(default_factory=utc_now_iso)

