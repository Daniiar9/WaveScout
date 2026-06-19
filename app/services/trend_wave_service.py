from __future__ import annotations

from app.models import TrendWave
from app.models.common import utc_now_iso
from app.services.storage import LocalJSONStorage
from app.services.text import stable_id


def list_trend_waves(storage: LocalJSONStorage | None = None) -> list[TrendWave]:
    return (storage or LocalJSONStorage()).load_waves()


def create_trend_wave(payload: dict, storage: LocalJSONStorage | None = None) -> TrendWave:
    storage = storage or LocalJSONStorage()
    wave = TrendWave(
        id=payload.get("id") or stable_id("wave", payload["name"]),
        name=payload["name"],
        category=payload.get("category", ""),
        keywords=payload.get("keywords", []),
        hashtags=payload.get("hashtags", []),
        adjacent_topics=payload.get("adjacent_topics", []),
        description=payload.get("description", ""),
        product_relevance=payload.get("product_relevance", ""),
        why_now=payload.get("why_now", ""),
        example_video_urls=payload.get("example_video_urls", []),
        example_creator_handles=payload.get("example_creator_handles", []),
        confidence=float(payload.get("confidence", 0.5)),
        created_at=payload.get("created_at", utc_now_iso()),
        updated_at=utc_now_iso(),
    )
    waves = storage.load_waves()
    waves = [existing for existing in waves if existing.id != wave.id]
    waves.append(wave)
    storage.save_waves(waves)
    return wave

