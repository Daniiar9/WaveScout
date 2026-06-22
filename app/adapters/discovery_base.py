from __future__ import annotations

from dataclasses import dataclass, field

from app.models import CreatorSearchStrategy, DiscoveryCandidate


@dataclass
class DiscoveryAdapterResult:
    adapter_name: str
    live: bool = False
    external_calls_made: bool = False
    candidates: list[DiscoveryCandidate] = field(default_factory=list)
    dry_run_payloads: list[dict] = field(default_factory=list)
    status: str = "dry_run"
    reason: str = ""


class DiscoveryAdapter:
    name = "base"
    supports_live = False
    requires_external_calls = False
    required_config: list[str] = []

    def discover_candidates(
        self,
        strategy: CreatorSearchStrategy,
        limit: int,
        live: bool = False,
    ) -> DiscoveryAdapterResult:
        raise NotImplementedError

