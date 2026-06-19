from __future__ import annotations

import argparse
import csv
from collections import defaultdict

from bootstrap import bootstrap

bootstrap()

from app.services.creator_discovery import import_comment_samples
from app.services.storage import LocalJSONStorage


def import_csv(path: str) -> int:
    storage = LocalJSONStorage()
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            creator = storage.find_creator(row["creator_handle"])
            if not creator:
                raise SystemExit(f"Creator not found in local data: {row['creator_handle']}")
            grouped[(creator.id, row.get("video_url", ""))].append(row["comment_text"])
    total = 0
    for (creator_id, video_url), comments in grouped.items():
        import_comment_samples(creator_id, comments, video_url=video_url, storage=storage)
        total += len(comments)
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Import comment samples from CSV.")
    parser.add_argument("csv_path")
    args = parser.parse_args()
    total = import_csv(args.csv_path)
    print(f"Imported {total} comments into local JSON storage.")


if __name__ == "__main__":
    main()

