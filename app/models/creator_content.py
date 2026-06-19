from __future__ import annotations

from dataclasses import dataclass, field


CONTENT_FORMATS = {
    "demo",
    "reaction",
    "tutorial",
    "teardown",
    "hot_take",
    "founder_pov",
    "comparison",
    "news_commentary",
    "other",
}


@dataclass
class CreatorContentSample:
    id: str
    creator_id: str
    video_url: str = ""
    title_or_caption: str = ""
    transcript_or_summary: str = ""
    hashtags: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    format: str = "other"
    views: int = 0
    likes: int = 0
    comments_count: int = 0
    posted_at: str = ""
    notes: str = ""

