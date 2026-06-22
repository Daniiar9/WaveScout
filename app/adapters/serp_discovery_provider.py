from __future__ import annotations

from app.config import AppConfig, load_config
from app.models import LiveDiscoveryRequest, LiveDiscoveryResponse
from app.services.live_discovery_gate import (
    check_live_discovery_provider,
    run_serp_discovery,
)


def check_serp_provider(config: AppConfig | None = None, allow_external: bool = False) -> dict:
    return check_live_discovery_provider("serp", config or load_config(), allow_external=allow_external)


def run_serp_provider(request: LiveDiscoveryRequest, config: AppConfig | None = None) -> LiveDiscoveryResponse:
    return run_serp_discovery(request, config or load_config())
