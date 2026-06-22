from __future__ import annotations

from pathlib import Path

from app.adapters.discovery_base import DiscoveryAdapter, DiscoveryAdapterResult
from app.models import CreatorCandidate, CreatorSearchStrategy, DiscoveryCandidate
from app.services.storage import coerce_dataclass
from app.services.text import unique_keep_order
import json


class ManualDiscovery(DiscoveryAdapter):
    name = "manual_import"
    supports_live = False
    requires_external_calls = False
    required_config: list[str] = []

    def __init__(self, creators_path: str | None = "data/imported_creators.json") -> None:
        self.creators_path = creators_path

    def discover_candidates(
        self,
        strategy: CreatorSearchStrategy,
        limit: int,
        live: bool = False,
    ) -> DiscoveryAdapterResult:
        candidates: list[DiscoveryCandidate] = []
        path = Path(self.creators_path or "")
        if path.exists():
            creators = [coerce_dataclass(CreatorCandidate, item) for item in json.loads(path.read_text(encoding="utf-8"))]
            for creator in creators[:limit]:
                candidates.append(
                    DiscoveryCandidate(
                        handle=creator.handle,
                        profile_url=creator.profile_url,
                        source=self.name,
                        matched_query=strategy.search_queries[0] if strategy.search_queries else "",
                        matched_wave=strategy.trend_waves[0] if strategy.trend_waves else "",
                        matched_hashtags=unique_keep_order(creator.hashtags_used + strategy.hashtags, 5),
                        reason_found="Imported manually by human researcher.",
                        raw_snippet=creator.bio,
                        confidence=0.65,
                        requires_manual_review=True,
                    )
                )
        return DiscoveryAdapterResult(
            adapter_name=self.name,
            live=False,
            external_calls_made=False,
            candidates=candidates,
            dry_run_payloads=[],
            status="available" if candidates else "no_imported_candidates",
            reason="Manual import is offline and requires human-provided CSV/JSON data.",
        )

