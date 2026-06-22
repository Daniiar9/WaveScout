from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import AppConfig
from app.adapters.serp_discovery_provider import check_serp_provider, run_serp_provider
from app.services.live_discovery_gate import build_live_discovery_request
from app.services.scout_planner import build_scout_run_plan


def main() -> None:
    plan = build_scout_run_plan(product_text="An AI workspace for connected workflows.")
    request = build_live_discovery_request(plan.search_strategy, provider="serp", limit=3)
    response = run_serp_provider(request, AppConfig())
    assert response.provider == "serp"
    assert response.external_calls is False
    assert response.payloads
    status = check_serp_provider(AppConfig(), allow_external=False)
    assert status["allowed"] is False
    assert status["safety_status"]["tiktok_scraping"] is False
    print("test_serp_discovery_provider passed")


if __name__ == "__main__":
    main()
