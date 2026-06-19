from __future__ import annotations

import hashlib
import re
from collections import Counter
from typing import Iterable


def stable_id(prefix: str, *parts: object) -> str:
    raw = "|".join(str(part) for part in parts if part is not None)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}_{digest}"


def normalize_handle(handle: str) -> str:
    value = handle.strip()
    if not value:
        return ""
    return value if value.startswith("@") else f"@{value}"


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def weighted_overlap(left: Iterable[str], right_text: str) -> int:
    right = tokenize(right_text)
    return sum(1 for item in left if tokenize(item) & right)


def top_items(values: Iterable[str], limit: int = 5) -> list[str]:
    clean = [value for value in values if value]
    return [item for item, _count in Counter(clean).most_common(limit)]


def unique_keep_order(values: Iterable[str], limit: int | None = None) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
        if limit is not None and len(result) >= limit:
            break
    return result

