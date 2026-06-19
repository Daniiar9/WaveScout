from __future__ import annotations

from dataclasses import dataclass, field

from app.models.common import utc_now_iso


FIT_STATUSES = {
    "new",
    "shortlisted",
    "rejected",
    "contacted",
    "replied",
    "interested",
    "not_fit",
    "archived",
}


@dataclass
class CreatorCandidate:
    id: str
    handle: str
    display_name: str = ""
    profile_url: str = ""
    bio: str = ""
    follower_count: int = 0
    avg_views: int = 0
    avg_likes: int = 0
    engagement_notes: str = ""
    categories: list[str] = field(default_factory=list)
    hashtags_used: list[str] = field(default_factory=list)
    recent_video_urls: list[str] = field(default_factory=list)
    recent_video_summaries: list[str] = field(default_factory=list)
    email_or_contact: str = ""
    region: str = ""
    language: str = "en"
    fit_status: str = "new"
    source: str = "manual"
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

