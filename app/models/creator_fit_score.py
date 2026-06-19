from __future__ import annotations

from dataclasses import dataclass, field


FIT_LEVELS = {"high", "medium", "low", "reject"}


@dataclass
class CreatorFitScore:
    creator_id: str
    trend_wave_id: str
    score: int
    fit_level: str
    topical_relevance: int = 0
    audience_relevance: int = 0
    comment_intent_quality: int = 0
    creator_trust_clarity: int = 0
    product_demo_fit: int = 0
    commercial_priority: int = 0
    risk_penalty: int = 0
    reasons: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    best_angle: str = ""
    suggested_offer: str = ""
    outreach_priority: str = "hold"

