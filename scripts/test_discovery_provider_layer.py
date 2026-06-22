from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.services.discovery_provider_service import (
    check_discovery_provider,
    list_discovery_providers,
    run_discovery_provider_dry_run,
)
from app.services.scout_planner import build_scout_run_plan


def main() -> None:
    providers = list_discovery_providers()
    assert len(providers) >= 5
    assert any(provider.name == "manual_import" for provider in providers)
    assert all(provider.status for provider in providers)
    provider = check_discovery_provider("dry_run_search")
    plan = build_scout_run_plan(product_text="An AI workspace that connects your apps into workflows.")
    result = run_discovery_provider_dry_run(provider, plan.search_strategy, limit=10, scout_plan_id=plan.id)
    assert result.dry_run is True
    assert result.external_calls is False
    assert result.payload["dry_run_payloads"]
    print("test_discovery_provider_layer passed")


if __name__ == "__main__":
    main()

