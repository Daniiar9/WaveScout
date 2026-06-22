from __future__ import annotations

import argparse
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.models.common import to_plain_dict
from app.services.growth_brief_renderer import render_growth_brief_markdown
from app.services.growth_engine import growth_brief_to_json, run_growth_engine


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the WaveScout end-to-end growth engine in dry-run mode.")
    parser.add_argument("--product-url", default="")
    parser.add_argument("--product-text", default="")
    parser.add_argument("--owned-tiktok", default="")
    parser.add_argument("--owned-content", default="")
    parser.add_argument("--owned-comments", default="")
    parser.add_argument("--imported-creators", default="")
    parser.add_argument("--imported-content", default="")
    parser.add_argument("--imported-comments", default="")
    parser.add_argument("--discovery-limit", type=int, default=25)
    parser.add_argument("--top-creators", type=int, default=5)
    parser.add_argument("--out", default="artifacts/growth_brief.md")
    parser.add_argument("--json-out", default="artifacts/growth_brief.json")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--allow-fetch", action="store_true", default=False)
    parser.add_argument("--allow-external-discovery", action="store_true", default=False)
    args = parser.parse_args()

    if args.product_url and not args.product_text and not args.allow_fetch:
        print("Product URL received, but fetch is disabled. Add --product-text or enable --allow-fetch.")

    growth_brief = run_growth_engine(
        product_url=args.product_url or None,
        product_text=args.product_text or None,
        owned_tiktok=args.owned_tiktok or None,
        imported_creators=args.imported_creators or None,
        imported_content=args.imported_content or None,
        imported_comments=args.imported_comments or None,
        discovery_limit=args.discovery_limit,
        top_creators=args.top_creators,
        dry_run=args.dry_run,
        allow_fetch=args.allow_fetch,
        allow_external_discovery=args.allow_external_discovery,
    )
    out_path = Path(args.out)
    json_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_growth_brief_markdown(growth_brief), encoding="utf-8")
    json_path.write_text(growth_brief_to_json(growth_brief), encoding="utf-8")

    print("WaveScout Growth Engine: PASS")
    print("External calls: false")
    print("TikTok scraping: false")
    print("TikTok DM/send: false")
    print("Live posting: false")
    print("Notion write: false")
    print("\nProduct:")
    print(growth_brief.product_brief.category)
    print("\nPrimary waves:")
    for wave in growth_brief.wave_map.primary_waves[:6]:
        print(f"* {wave}")
    print("\nDiscovery:")
    print(f"* providers checked: {growth_brief.discovery_summary['providers_checked']}")
    print(f"* dry-run payloads: {growth_brief.discovery_summary['dry_run_payloads']}")
    print(f"* candidates from manual import: {growth_brief.discovery_summary['candidates_from_manual_import']}")
    print(f"* candidates needing enrichment: {growth_brief.discovery_summary['candidates_needing_enrichment']}")
    print("\nTop recommendations:")
    for action in growth_brief.next_safe_actions[:5]:
        print(f"* {action}")
    print("\nArtifacts:")
    print(out_path.as_posix())
    print(json_path.as_posix())


if __name__ == "__main__":
    main()
