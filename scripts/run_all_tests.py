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

