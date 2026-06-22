from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

COMMANDS = [
    ["scripts/demo_tiktok_growth_workflow.py"],
    ["scripts/test_tiktok_growth_workflow.py"],
    ["scripts/test_creator_scoring.py"],
    ["scripts/test_comment_intelligence.py"],
    ["scripts/test_audience_analysis.py"],
    ["scripts/test_notion_sync_dryrun.py"],
    ["scripts/test_mcp_tools_import.py"],
    ["scripts/test_real_creator_import_workflow.py"],
    ["scripts/test_tiktok_capability_service.py"],
    ["scripts/test_tiktok_adapters_dryrun.py"],
    ["scripts/test_tiktok_mcp_tools.py"],
    ["scripts/test_product_intelligence.py"],
    ["scripts/test_trend_wave_mapper.py"],
    ["scripts/test_creator_search_strategy.py"],
    ["scripts/test_owned_tiktok_analysis.py"],
    ["scripts/test_scout_planner.py"],
    ["scripts/test_discovery_dryrun.py"],
    ["scripts/test_discovery_provider_layer.py"],
    ["scripts/test_discovery_candidate_normalizer.py"],
    ["scripts/test_growth_engine.py"],
    ["scripts/test_growth_brief_renderer.py"],
    ["scripts/test_notion_pipeline_builder.py"],
    ["scripts/test_feedback_loop.py"],
    ["scripts/test_growth_engine_mcp_tools.py"],
    ["-m", "compileall", "app", "scripts"],
]


def main() -> None:
    print("WaveScout test runner")
    for args in COMMANDS:
        display = "python " + " ".join(args)
        print(f"\nRunning: {display}")
        completed = subprocess.run([sys.executable, *args], cwd=ROOT, check=False)
        if completed.returncode != 0:
            raise SystemExit(completed.returncode)
    print("\nWaveScout tests: PASS")


if __name__ == "__main__":
    main()
