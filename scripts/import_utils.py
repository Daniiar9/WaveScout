from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Iterable

from app.models.common import to_plain_dict
from app.services.text import normalize_handle, stable_id


def read_csv_rows(path: str | Path, expected_columns: Iterable[str]) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = [column for column in expected_columns if column not in columns]
        if missing:
            raise SystemExit(f"Missing required columns: {', '.join(missing)}")
        return [dict(row) for row in reader]


def write_json(path: str | Path, payload: object) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(to_plain_dict(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def split_multi(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in re.split(r"[;,]", str(value)) if item.strip()]


def to_int(value: object, default: int = 0) -> int:
    if value is None or str(value).strip() == "":
        return default
    try:
        return int(float(str(value).replace(",", "").strip()))
    except ValueError:
        return default


def normalized_handle(value: object) -> str:
    return normalize_handle(str(value or "").strip())


def creator_id_for_handle(handle: str) -> str:
    return stable_id("creator", normalized_handle(handle))


def safe_filename_for_handle(handle: str, suffix: str) -> str:
    cleaned = normalized_handle(handle).lstrip("@").lower()
    cleaned = re.sub(r"[^a-z0-9._-]+", "_", cleaned).strip("_")
    return f"{cleaned or 'creator'}_{suffix}"


def row_has_required(row: dict, required_fields: Iterable[str]) -> bool:
    return all(str(row.get(field, "")).strip() for field in required_fields)

