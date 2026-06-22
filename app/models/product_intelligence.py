from __future__ import annotations

from dataclasses import dataclass, field

from app.models.common import utc_now_iso


@dataclass
class ProductIntelligenceBrief:
    id: str
    product_url: str = ""
    product_name: str = ""
    one_liner: str = ""
    category: str = ""
    target_users: list[str] = field(default_factory=list)
    target_buyers: list[str] = field(default_factory=list)
    core_use_cases: list[str] = field(default_factory=list)
    pain_points: list[str] = field(default_factory=list)
    value_props: list[str] = field(default_factory=list)
    differentiators: list[str] = field(default_factory=list)
    proof_points: list[str] = field(default_factory=list)
    competitors_or_alternatives: list[str] = field(default_factory=list)
    trend_keywords: list[str] = field(default_factory=list)
    creator_relevant_angles: list[str] = field(default_factory=list)
    avoid_positioning: list[str] = field(default_factory=list)
    confidence: float = 0.0
    evidence: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)


@dataclass
class TrendWaveMap:
    id: str
    product_id: str
    primary_waves: list[str] = field(default_factory=list)
    adjacent_waves: list[str] = field(default_factory=list)
    rejected_waves: list[str] = field(default_factory=list)
    wave_relevance_reasons: dict[str, str] = field(default_factory=dict)
    hashtags: list[str] = field(default_factory=list)
    search_keywords: list[str] = field(default_factory=list)
    creator_archetypes: list[str] = field(default_factory=list)
    why_now: str = ""
    confidence: float = 0.0

