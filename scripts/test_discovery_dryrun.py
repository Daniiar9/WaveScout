from __future__ import annotations

import tempfile
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.services.scout_planner import build_scout_run_plan, render_discovery_queries_markdown, run_discovery_dry_run

PRODUCT_TEXT = "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows."


def main() -> None:
    plan = build_scout_run_plan(product_text=PRODUCT_TEXT)
    results = run_discovery_dry_run(plan, limit=25)
    assert results
    assert all(result["external_calls_made"] is False for result in results)
    assert plan.safety_status["tiktok_dm_send"] is False
    assert plan.safety_status["message_sending"] is False
    assert "search_provider_placeholder" in render_discovery_queries_markdown(plan)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "discovery_dryrun.md"
        out.write_text(render_discovery_queries_markdown(plan), encoding="utf-8")
        assert out.exists()
    print("test_discovery_dryrun passed")


if __name__ == "__main__":
    main()

