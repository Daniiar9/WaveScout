from __future__ import annotations

import argparse

from bootstrap import bootstrap

bootstrap()

from app.models import CreatorCandidate
from scripts.import_utils import (
    creator_id_for_handle,
    normalized_handle,
    read_csv_rows,
    row_has_required,
    split_multi,
    to_int,
    write_json,
)

EXPECTED_COLUMNS = [
    "handle",
    "display_name",
    "profile_url",
    "bio",
    "follower_count",
    "avg_views",
    "avg_likes",
    "categories",
    "hashtags_used",
    "email_or_contact",
    "region",
    "language",
    "source",
    "notes",
]


def import_csv(input_path: str, out_path: str) -> tuple[list[CreatorCandidate], int]:
    rows = read_csv_rows(input_path, EXPECTED_COLUMNS)
    creators: list[CreatorCandidate] = []
    skipped = 0
    for row in rows:
        if not row_has_required(row, ["handle"]):
            skipped += 1
            continue
        handle = normalized_handle(row["handle"])
        creators.append(
            CreatorCandidate(
                id=creator_id_for_handle(handle),
                handle=handle,
                display_name=row.get("display_name", "").strip() or handle.lstrip("@"),
                profile_url=row.get("profile_url", "").strip(),
                bio=row.get("bio", "").strip(),
                follower_count=to_int(row.get("follower_count")),
                avg_views=to_int(row.get("avg_views")),
                avg_likes=to_int(row.get("avg_likes")),
                engagement_notes=row.get("notes", "").strip(),
                categories=split_multi(row.get("categories")),
                hashtags_used=split_multi(row.get("hashtags_used")),
                email_or_contact=row.get("email_or_contact", "").strip(),
                region=row.get("region", "").strip(),
                language=row.get("language", "").strip() or "en",
                fit_status="new",
                source=row.get("source", "").strip() or "manual_import",
            )
        )
    write_json(out_path, creators)
    return creators, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Import creator candidates from CSV into local JSON.")
    parser.add_argument("csv_path", nargs="?", help="Deprecated positional input path; prefer --input.")
    parser.add_argument("--input", dest="input_path", help="CSV input path.")
    parser.add_argument("--out", default="data/imported_creators.json", help="JSON output path.")
    args = parser.parse_args()
    input_path = args.input_path or args.csv_path
    if not input_path:
        raise SystemExit("Provide --input path.")
    creators, skipped = import_csv(input_path, args.out)
    print(f"imported creators: {len(creators)}")
    print(f"skipped rows: {skipped}")
    print(f"output: {args.out}")


if __name__ == "__main__":
    main()

