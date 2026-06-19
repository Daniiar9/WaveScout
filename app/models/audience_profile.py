from __future__ import annotations

from dataclasses import dataclass, field


AUDIENCE_QUALITY_LEVELS = {
    "high_intent",
    "useful_awareness",
    "mixed",
    "low_quality",
    "irrelevant",
}


@dataclass
class AudienceProfile:
    creator_id: str
    likely_audience_segments: list[str] = field(default_factory=list)
    buyer_intent_summary: str = ""
    common_questions: list[str] = field(default_factory=list)
    common_pains: list[str] = field(default_factory=list)
    objections: list[str] = field(default_factory=list)
    tool_mentions: list[str] = field(default_factory=list)
    audience_quality_level: str = "mixed"
    audience_fit_score: int = 0
    confidence: float = 0.0

