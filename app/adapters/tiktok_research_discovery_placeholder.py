from __future__ import annotations

from app.adapters.discovery_base import DiscoveryAdapter, DiscoveryAdapterResult
from app.config import AppConfig, load_config
from app.models import CreatorSearchStrategy
from app.models.common import to_plain_dict
from app.services.tiktok_capability_service import check_capability


class TikTokResearchDiscoveryPlaceholder(DiscoveryAdapter):
    name = "official_tiktok_research_placeholder"
    supports_live = False
    requires_external_calls = True
    required_config = ["TIKTOK_OFFICIAL_API_ENABLED", "TIKTOK_RESEARCH_API_ENABLED", "research.data.basic"]

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or load_config()

    def discover_candidates(
        self,
        strategy: CreatorSearchStrategy,
        limit: int,
        live: bool = False,
    ) -> DiscoveryAdapterResult:
        capability = check_capability("research_query_videos", self.config)
        payloads = [
            {
                "capability": "research_query_videos",
                "query": {"keyword": keyword},
                "hashtags": strategy.hashtags[:8],
                "limit": min(limit, 25),
                "gate": to_plain_dict(capability.action_gate),
                "live_allowed": False,
            }
            for keyword in strategy.keywords[:8]
        ]
        return DiscoveryAdapterResult(
            adapter_name=self.name,
            live=False,
            external_calls_made=False,
            candidates=[],
            dry_run_payloads=payloads,
            status="blocked" if capability.status == "blocked" else "dry_run_only",
            reason=capability.reason,
        )

