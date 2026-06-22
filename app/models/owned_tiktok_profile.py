from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OwnedTikTokProfile:
    handle: str
    profile_url: str = ""
    bio: str = ""
    content_themes: list[str] = field(default_factory=list)
    top_hooks: list[str] = field(default_factory=list)
    top_formats: list[str] = field(default_factory=list)
    audience_questions: list[str] = field(default_factory=list)
    audience_pains: list[str] = field(default_factory=list)
    comment_intelligence_summary: dict = field(default_factory=dict)
    content_gaps: list[str] = field(default_factory=list)
    creator_collab_opportunities: list[str] = field(default_factory=list)
    brand_voice_notes: list[str] = field(default_factory=list)
    best_performing_angles: list[str] = field(default_factory=list)
    avoid_repeating: list[str] = field(default_factory=list)
    confidence: float = 0.0

