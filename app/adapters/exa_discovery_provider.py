from __future__ import annotations

from app.config import AppConfig, load_config
from app.models import LiveDiscoveryRequest, LiveDiscoveryResponse
from app.services.live_discovery_gate import (
    check_live_discovery_provider,
    run_exa_discovery,
)


def check_exa_provider(config: AppConfig | None = None, allow_external: bool = False) -> dict:
    return check_live_discovery_provider("exa", config or load_config(), allow_external=allow_external)


def run_exa_provider(request: LiveDiscoveryRequest, config: AppConfig | None = None) -> LiveDiscoveryResponse:
    return run_exa_discovery(request, config or load_config())
