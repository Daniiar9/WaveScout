from __future__ import annotations

import tempfile
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.services.scout_planner import build_scout_run_plan, render_scout_plan_json, render_scout_run_plan_markdown

PRODUCT_TEXT = "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows."


def main() -> None:
    plan = build_scout_run_plan(product_text=PRODUCT_TEXT, owned_tiktok_handle="@demoapp")
    assert plan.product_brief.category == "AI workspace / connected SaaS stack"
    assert plan.owned_tiktok_profile_optional is not None
    assert plan.search_strategy.search_queries
    assert plan.safety_status["external_calls"] is False
    assert plan.safety_status["tiktok_scraping"] is False
    markdown = render_scout_run_plan_markdown(plan)
    assert "WaveScout Product-Led Scout Plan" in markdown
    assert "Safety Status" in markdown
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "scout_plan.md"
        out.write_text(markdown, encoding="utf-8")
        assert out.exists()
    assert '"external_calls": false' in render_scout_plan_json(plan)
    print("test_scout_planner passed")


if __name__ == "__main__":
    main()

