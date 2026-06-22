from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import AppConfig
from app.services.live_discovery_gate import (
    build_live_discovery_request,
    check_live_discovery_provider,
    run_live_discovery_request,
)
from app.services.scout_planner import build_scout_run_plan


def main() -> None:
    plan = build_scout_run_plan(product_text="An AI workspace for connected workflows.")
    request = build_live_discovery_request(plan.search_strategy, provider="exa", limit=5)
    response = run_live_discovery_request(request, AppConfig())
    assert response.dry_run is True
    assert response.external_calls is False
    assert response.payloads
    assert response.safety_status["send_allowed"] is False
    assert response.safety_status["tiktok_scraping"] is False

    live_check = check_live_discovery_provider(
        "exa",
        AppConfig(wavescout_allow_external_calls=True),
        allow_external=True,
    )
    assert live_check["allowed"] is False
    assert live_check["external_calls"] is False
    assert "EXA_API_KEY" in live_check["missing_env_vars"]
    print("test_live_discovery_gate passed")


if __name__ == "__main__":
    main()
