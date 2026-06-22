from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from bootstrap import bootstrap

ROOT = bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from app.models import CreatorContentSample
from app.services.scout_planner import build_scout_run_plan, render_scout_plan_json, render_scout_run_plan_markdown
from app.services.storage import coerce_dataclass
from scripts.import_utils import creator_id_for_handle, split_multi, stable_id, to_int


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a product-led creator scout plan.")
    parser.add_argument("--product-url", default="")
    parser.add_argument("--product-text", default="")
    parser.add_argument("--owned-tiktok", default="")
    parser.add_argument("--owned-content", default="")
    parser.add_argument("--owned-comments", default="")
    parser.add_argument("--allow-fetch", action="store_true", default=False)
    parser.add_argument("--out", default="artifacts/scout_plan.md")
    parser.add_argument("--json-out", default="")
    parser.add_argument("--dry-run", action="store_true", default=True)
    args = parser.parse_args()

    plan = build_scout_run_plan(
        product_url=args.product_url or None,
        product_text=args.product_text or None,
        owned_tiktok_handle=args.owned_tiktok or None,
        owned_content=_load_owned_content(args.owned_content),
        owned_comments=_load_owned_comments(args.owned_comments),
        allow_fetch=args.allow_fetch,
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_scout_run_plan_markdown(plan), encoding="utf-8")
    json_out = Path(args.json_out) if args.json_out else out_path.with_suffix(".json")
    json_out.write_text(render_scout_plan_json(plan), encoding="utf-8")

    print("WaveScout Scout Planner: PASS")
    print("External calls: false")
    print(f"Product fetch: {str(plan.safety_status.get('product_fetch', False)).lower()}")
    print("TikTok live calls: false")
    print("TikTok scraping: false")
    print("TikTok DM/send: false")
    print("\nProduct:")
    print(plan.product_brief.category)
    print("\nPrimary waves:")
    for wave in plan.wave_map.primary_waves[:6]:
        print(f"* {wave}")
    print("\nCreator archetypes:")
    for archetype in plan.search_strategy.creator_archetypes[:5]:
        print(f"* {archetype}")
    print("\nArtifact:")
    print(out_path.as_posix())


def _load_owned_content(path: str) -> list[CreatorContentSample]:
    if not path:
        return []
    input_path = Path(path)
    if input_path.suffix.lower() == ".json":
        return [coerce_dataclass(CreatorContentSample, item) for item in json.loads(input_path.read_text(encoding="utf-8"))]
    with input_path.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        samples = []
        for index, row in enumerate(rows):
            handle = row.get("creator_handle") or row.get("handle") or "owned"
            creator_id = creator_id_for_handle(handle)
            video_url = row.get("video_url", "")
            samples.append(
                CreatorContentSample(
                    id=stable_id("owned_content", creator_id, video_url, index),
                    creator_id=creator_id,
                    video_url=video_url,
                    title_or_caption=row.get("title_or_caption", ""),
                    transcript_or_summary=row.get("transcript_or_summary", ""),
                    hashtags=split_multi(row.get("hashtags", "")),
                    topics=split_multi(row.get("topics", "")),
                    format=row.get("format", "other") or "other",
                    views=to_int(row.get("views", 0)),
                    likes=to_int(row.get("likes", 0)),
                    comments_count=to_int(row.get("comments_count", 0)),
                    posted_at=row.get("posted_at", ""),
                    notes=row.get("notes", ""),
                )
            )
        return samples


def _load_owned_comments(path: str) -> list[str | dict]:
    if not path:
        return []
    input_path = Path(path)
    if input_path.suffix.lower() == ".json":
        return json.loads(input_path.read_text(encoding="utf-8"))
    with input_path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle)]


if __name__ == "__main__":
    main()

