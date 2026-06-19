from __future__ import annotations

from dataclasses import dataclass, field

from app.models.common import utc_now_iso


@dataclass
class TrendWave:
    id: str
    name: str
    category: str = ""
    keywords: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    adjacent_topics: list[str] = field(default_factory=list)
    description: str = ""
    product_relevance: str = ""
    why_now: str = ""
    example_video_urls: list[str] = field(default_factory=list)
    example_creator_handles: list[str] = field(default_factory=list)
    confidence: float = 0.0
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

