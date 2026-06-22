from __future__ import annotations

from dataclasses import dataclass, field

from app.models.creator_search_strategy import CreatorSearchStrategy
from app.models.owned_tiktok_profile import OwnedTikTokProfile
from app.models.product_intelligence import ProductIntelligenceBrief, TrendWaveMap


@dataclass
class ScoutRunPlan:
    id: str
    product_brief: ProductIntelligenceBrief
    wave_map: TrendWaveMap
    search_strategy: CreatorSearchStrategy
    owned_tiktok_profile_optional: OwnedTikTokProfile | None = None
    discovery_adapters: list[dict] = field(default_factory=list)
    dry_run_queries: list[dict] = field(default_factory=list)
    expected_inputs: list[str] = field(default_factory=list)
    expected_outputs: list[str] = field(default_factory=list)
    safety_status: dict = field(default_factory=dict)
    next_safe_actions: list[str] = field(default_factory=list)

