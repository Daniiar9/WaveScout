from __future__ import annotations

import argparse

from bootstrap import bootstrap

bootstrap()

from scripts.import_utils import (
    creator_id_for_handle,
    read_csv_rows,
    row_has_required,
    stable_id,
    write_json,
)

EXPECTED_COLUMNS = ["creator_handle", "video_url", "comment_text", "notes"]


def import_csv(input_path: str, out_path: str) -> tuple[list[dict], int]:
    rows = read_csv_rows(input_path, EXPECTED_COLUMNS)
    comments: list[dict] = []
    skipped = 0
    for index, row in enumerate(rows):
        if not row_has_required(row, ["creator_handle", "comment_text"]):
            skipped += 1
            continue
        creator_id = creator_id_for_handle(row["creator_handle"])
        video_url = row.get("video_url", "").strip()
        text = row.get("comment_text", "").strip()
        comments.append(
            {
                "id": stable_id("raw_comment", creator_id, video_url, text, index),
                "creator_id": creator_id,
                "video_url": video_url,
                "comment_text": text,
                "notes": row.get("notes", "").strip(),
                "source": "manual_import",
            }
        )
    write_json(out_path, comments)
    return comments, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Import comment samples from CSV into local JSON.")
    parser.add_argument("csv_path", nargs="?", help="Deprecated positional input path; prefer --input.")
    parser.add_argument("--input", dest="input_path", help="CSV input path.")
    parser.add_argument("--out", default="data/imported_comments.json", help="JSON output path.")
    args = parser.parse_args()
    input_path = args.input_path or args.csv_path
    if not input_path:
        raise SystemExit("Provide --input path.")
    comments, skipped = import_csv(input_path, args.out)
    print(f"imported comments: {len(comments)}")
    print(f"skipped rows: {skipped}")
    print(f"output: {args.out}")


if __name__ == "__main__":
    main()

