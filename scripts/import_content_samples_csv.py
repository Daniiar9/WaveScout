from __future__ import annotations

import argparse

from bootstrap import bootstrap

bootstrap()

from app.models import CreatorContentSample
from scripts.import_utils import (
    creator_id_for_handle,
    read_csv_rows,
    row_has_required,
    split_multi,
    stable_id,
    to_int,
    write_json,
)

EXPECTED_COLUMNS = [
    "creator_handle",
    "video_url",
    "title_or_caption",
    "transcript_or_summary",
    "hashtags",
    "topics",
    "format",
    "views",
    "likes",
    "comments_count",
    "posted_at",
    "notes",
]


def import_csv(input_path: str, out_path: str) -> tuple[list[CreatorContentSample], int]:
    rows = read_csv_rows(input_path, EXPECTED_COLUMNS)
    samples: list[CreatorContentSample] = []
    skipped = 0
    for row in rows:
        if not row_has_required(row, ["creator_handle", "video_url"]):
            skipped += 1
            continue
        creator_id = creator_id_for_handle(row["creator_handle"])
        video_url = row.get("video_url", "").strip()
        samples.append(
            CreatorContentSample(
                id=stable_id("content", creator_id, video_url),
                creator_id=creator_id,
                video_url=video_url,
                title_or_caption=row.get("title_or_caption", "").strip(),
                transcript_or_summary=row.get("transcript_or_summary", "").strip(),
                hashtags=split_multi(row.get("hashtags")),
                topics=split_multi(row.get("topics")),
                format=row.get("format", "").strip() or "other",
                views=to_int(row.get("views")),
                likes=to_int(row.get("likes")),
                comments_count=to_int(row.get("comments_count")),
                posted_at=row.get("posted_at", "").strip(),
                notes=row.get("notes", "").strip(),
            )
        )
    write_json(out_path, samples)
    return samples, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Import creator content samples from CSV into local JSON.")
    parser.add_argument("--input", required=True, help="CSV input path.")
    parser.add_argument("--out", default="data/imported_content_samples.json", help="JSON output path.")
    args = parser.parse_args()
    samples, skipped = import_csv(args.input, args.out)
    print(f"imported content samples: {len(samples)}")
    print(f"skipped rows: {skipped}")
    print(f"output: {args.out}")


if __name__ == "__main__":
    main()

