from __future__ import annotations

from dataclasses import dataclass, field

from app.models.common import utc_now_iso


@dataclass
class CreatorSearchStrategy:
    id: str
    product_id: str
    trend_waves: list[str] = field(default_factory=list)
    creator_archetypes: list[str] = field(default_factory=list)
    search_queries: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    content_formats_to_target: list[str] = field(default_factory=list)
    comment_patterns_to_look_for: list[str] = field(default_factory=list)
    qualification_criteria: list[str] = field(default_factory=list)
    rejection_criteria: list[str] = field(default_factory=list)
    outreach_angles: list[str] = field(default_factory=list)
    priority_order: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)

