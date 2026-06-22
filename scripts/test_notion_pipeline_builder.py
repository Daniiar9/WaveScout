from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.services.growth_engine import run_growth_engine
from app.services.notion_pipeline_builder import build_growth_brief_notion_payload, build_notion_pipeline_payloads, render_notion_pipeline_markdown


def main() -> None:
    growth_brief = run_growth_engine(product_text="An AI workspace that connects your apps into workflows.")
    payload = build_notion_pipeline_payloads(growth_brief)
    assert payload["dry_run"] is True
    assert payload["notion_write"] is False
    assert payload["growth_brief"]["Send Allowed"] is False
    assert payload["growth_brief"]["Approval Required"] is True
    assert "Notion Dry-Run Pipeline" in render_notion_pipeline_markdown(payload)
    assert build_growth_brief_notion_payload(growth_brief)["External Calls"] is False
    print("test_notion_pipeline_builder passed")


if __name__ == "__main__":
    main()

