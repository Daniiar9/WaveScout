from __future__ import annotations

from dataclasses import dataclass, field

from app.models.discovery_provider import DiscoveryCandidateNormalized


@dataclass
class LiveDiscoveryRequest:
    provider: str
    queries: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    limit: int = 25
    allow_external: bool = False
    dry_run: bool = True
    product_context: str = ""
    safety_status: dict = field(default_factory=dict)


@dataclass
class LiveDiscoveryResponse:
    provider: str
    dry_run: bool = True
    external_calls: bool = False
    blocked_reason: str = ""
    payloads: list[dict] = field(default_factory=list)
    raw_results: list[dict] = field(default_factory=list)
    normalized_candidates: list[DiscoveryCandidateNormalized] = field(default_factory=list)
    safety_status: dict = field(default_factory=dict)
