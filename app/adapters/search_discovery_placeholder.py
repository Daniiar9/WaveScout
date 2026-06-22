from __future__ import annotations

from app.adapters.discovery_base import DiscoveryAdapter, DiscoveryAdapterResult
from app.models import CreatorSearchStrategy


class SearchDiscoveryPlaceholder(DiscoveryAdapter):
    name = "search_provider_placeholder"
    supports_live = False
    requires_external_calls = True
    required_config = ["WAVESCOUT_ALLOW_EXTERNAL_CALLS", "provider_api_key_placeholder"]

    def discover_candidates(
        self,
        strategy: CreatorSearchStrategy,
        limit: int,
        live: bool = False,
    ) -> DiscoveryAdapterResult:
        payloads = [
            {
                "query": query,
                "limit": min(limit, 10),
                "provider": self.name,
                "live_allowed": False,
            }
            for query in strategy.search_queries[: min(len(strategy.search_queries), 10)]
        ]
        return DiscoveryAdapterResult(
            adapter_name=self.name,
            live=False,
            external_calls_made=False,
            candidates=[],
            dry_run_payloads=payloads,
            status="dry_run_only",
            reason="Search provider integration is a placeholder. No external calls are made.",
        )

