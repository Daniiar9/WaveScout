from __future__ import annotations

from app.adapters.manual_import import build_content_sample_from_manual_import, build_creator_from_manual_import
from app.adapters.tiktok_url_parser import parse_tiktok_url
from app.models import CreatorCandidate, CreatorContentSample
from app.services.storage import LocalJSONStorage
from app.services.text import normalize_handle, stable_id


def import_creator_candidate(payload: dict, storage: LocalJSONStorage | None = None) -> CreatorCandidate:
    storage = storage or LocalJSONStorage()
    data = dict(payload)
    if not data.get("handle") and data.get("profile_url"):
        parsed = parse_tiktok_url(data["profile_url"])
        data["handle"] = parsed["handle"] or normalize_handle(data["profile_url"].split("/")[-1])
    creator = build_creator_from_manual_import(data)
    creators = storage.load_creators()
    creators = [existing for existing in creators if existing.id != creator.id and existing.handle != creator.handle]
    creators.append(creator)
    storage.save_creators(creators)
    return creator


def import_creator_content_sample(payload: dict, storage: LocalJSONStorage | None = None) -> CreatorContentSample:
    storage = storage or LocalJSONStorage()
    sample = build_content_sample_from_manual_import(payload)
    samples = storage.load_content_samples()
    samples = [existing for existing in samples if existing.id != sample.id]
    samples.append(sample)
    storage.save_content_samples(samples)
    return sample


def import_comment_samples(
    creator_id: str,
    comments: list[str],
    video_url: str = "",
    content_id: str | None = None,
    storage: LocalJSONStorage | None = None,
) -> list[dict]:
    storage = storage or LocalJSONStorage()
    current = storage.load_comments()
    imported = [
        {
            "id": stable_id("raw_comment", creator_id, content_id or video_url, text, index),
            "creator_id": creator_id,
            "content_id": content_id,
            "video_url": video_url,
            "comment_text": text,
            "source": "manual_import",
        }
        for index, text in enumerate(comments)
    ]
    current.extend(imported)
    storage.save_comments(current)
    return imported

