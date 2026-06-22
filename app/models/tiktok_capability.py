from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TikTokScopeRequirement:
    scope: str
    description: str = ""
    required_for: list[str] = field(default_factory=list)


@dataclass
class TikTokActionGate:
    capability_name: str
    allowed: bool
    reason: str
    required_scopes: list[str] = field(default_factory=list)
    missing_scopes: list[str] = field(default_factory=list)
    external_call_required: bool = True
    live_mode_required: bool = True
    human_approval_required: bool = True


@dataclass
class TikTokCapability:
    name: str
    description: str
    category: str
    official_api: str
    endpoint: str = ""
    use: str = ""
    required_scopes: list[str] = field(default_factory=list)
    config_flags: list[str] = field(default_factory=list)
    external_call_required: bool = True
    live_mode_supported: bool = False
    status: str = "dry_run_only"
    reason: str = ""
    docs_url: str = ""
    missing_scopes: list[str] = field(default_factory=list)
    missing_config_flags: list[str] = field(default_factory=list)
    action_gate: TikTokActionGate | None = None


@dataclass
class TikTokCapabilityReport:
    capabilities: list[TikTokCapability]
    approved_scopes: list[str] = field(default_factory=list)
    available: list[str] = field(default_factory=list)
    dry_run_only: list[str] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)
    not_configured: list[str] = field(default_factory=list)
    external_calls_made: bool = False
    scraping_enabled: bool = False
    dm_send_enabled: bool = False
    live_post_allowed: bool = False
    human_approval_required: bool = True
    summary: str = ""

