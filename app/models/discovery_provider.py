from __future__ import annotations

from dataclasses import dataclass, field

from app.models.common import utc_now_iso
from app.models.discovery_candidate import DiscoveryCandidate


@dataclass
class DiscoveryProvider:
    id: str
    name: str
    provider_type: str
    supports_live: bool = False
    requires_external_calls: bool = False
    required_env_vars: list[str] = field(default_factory=list)
    required_scopes: list[str] = field(default_factory=list)
    status: str = "dry_run_only"
    reason: str = ""
    safety_notes: list[str] = field(default_factory=list)


@dataclass
class DiscoveryCandidateNormalized:
    handle: str
    display_name: str = ""
    profile_url: str = ""
    platform: str = "tiktok"
    bio: str = ""
    matched_query: str = ""
    matched_wave: str = ""
    matched_hashtags: list[str] = field(default_factory=list)
    source_provider: str = ""
    source_confidence: float = 0.0
    reason_found: str = ""
    raw_snippet: str = ""
    requires_manual_review: bool = True
    created_at: str = field(default_factory=utc_now_iso)


@dataclass
class DiscoveryRunResult:
    id: str
    scout_plan_id: str
    provider: DiscoveryProvider
    query: str = ""
    dry_run: bool = True
    external_calls: bool = False
    candidates: list[DiscoveryCandidate] = field(default_factory=list)
    payload: dict = field(default_factory=dict)
    blocked_reason: str = ""
    created_at: str = field(default_factory=utc_now_iso)

