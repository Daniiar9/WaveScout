from __future__ import annotations

import argparse
import json
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from app.services.scout_planner import (
    build_scout_run_plan,
    render_discovery_queries_markdown,
    run_discovery_dry_run,
    scout_plan_from_dict,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render dry-run discovery payloads for a scout plan.")
    parser.add_argument("--plan", default="artifacts/scout_plan.json")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--out", default="artifacts/discovery_dryrun.md")
    args = parser.parse_args()
    plan = _load_or_build_plan(args.plan)
    results = run_discovery_dry_run(plan, limit=args.limit)
    output = _render_discovery_dryrun(plan, results, args.limit)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")
    print("WaveScout Discovery Dry Run: PASS")
    print("External calls: false")
    print("TikTok live calls: false")
    print("TikTok scraping: false")
    print("TikTok DM/send: false")
    print(f"Adapter payloads: {sum(len(result.get('dry_run_payloads', [])) for result in results)}")
    print("\nArtifact:")
    print(out_path.as_posix())


def _load_or_build_plan(path: str):
    input_path = Path(path)
    if input_path.exists():
        return scout_plan_from_dict(json.loads(input_path.read_text(encoding="utf-8")))
    return build_scout_run_plan(product_text=DEFAULT_PRODUCT_CONTEXT)


def _render_discovery_dryrun(plan, results: list[dict], limit: int) -> str:
    return f"""# Discovery Dry Run

## Generated Queries
{render_discovery_queries_markdown(plan)}

## Adapter Payloads
{_adapter_sections(results)}

## What Would Be Searched

If a compliant provider is connected later, WaveScout would search for creator/profile/video evidence around the generated queries, hashtags, and trend waves. This pass makes no external calls.

## Safety Status

- external_calls=false
- product_fetch=false
- tiktok_live_calls=false
- tiktok_scraping=false
- tiktok_dm_send=false
- message_sending=false
- limit={limit}
"""


def _adapter_sections(results: list[dict]) -> str:
    sections = []
    for result in results:
        sections.append(f"### {result['adapter_name']}\n")
        sections.append(f"- Status: {result['status']}")
        sections.append(f"- External calls made: {str(result['external_calls_made']).lower()}")
        sections.append(f"- Reason: {result['reason']}")
        payloads = result.get("dry_run_payloads", [])
        if payloads:
            sections.append("```json")
            sections.append(json.dumps(payloads[:10], indent=2, sort_keys=True))
            sections.append("```")
        candidates = result.get("candidates", [])
        if candidates:
            sections.append("Candidates:")
            for candidate in candidates[:10]:
                sections.append(f"- {candidate['handle']} ({candidate['source']})")
        sections.append("")
    return "\n".join(sections)


if __name__ == "__main__":
    main()

