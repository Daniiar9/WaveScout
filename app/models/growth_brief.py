from __future__ import annotations

from dataclasses import dataclass, field

from app.models.common import utc_now_iso
from app.models.creator_intelligence_packet import CreatorIntelligencePacket
from app.models.creator_search_strategy import CreatorSearchStrategy
from app.models.discovery_provider import DiscoveryCandidateNormalized
from app.models.owned_tiktok_profile import OwnedTikTokProfile
from app.models.product_intelligence import ProductIntelligenceBrief, TrendWaveMap


@dataclass
class GrowthBrief:
    id: str
    product_brief: ProductIntelligenceBrief
    wave_map: TrendWaveMap
    owned_tiktok_profile: OwnedTikTokProfile | None
    search_strategy: CreatorSearchStrategy
    discovery_summary: dict
    candidate_shortlist: list[DiscoveryCandidateNormalized] = field(default_factory=list)
    top_creator_packets: list[CreatorIntelligencePacket] = field(default_factory=list)
    content_recommendations: list[str] = field(default_factory=list)
    outreach_recommendations: list[str] = field(default_factory=list)
    notion_pipeline_payload: dict = field(default_factory=dict)
    missing_data: list[str] = field(default_factory=list)
    next_safe_actions: list[str] = field(default_factory=list)
    safety_status: dict = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

