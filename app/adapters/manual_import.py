from __future__ import annotations

from app.models import CreatorCandidate, CreatorContentSample
from app.services.text import normalize_handle, stable_id


def build_creator_from_manual_import(payload: dict) -> CreatorCandidate:
    handle = normalize_handle(payload.get("handle") or payload.get("profile_url", ""))
    return CreatorCandidate(
        id=payload.get("id") or stable_id("creator", handle),
        handle=handle,
        display_name=payload.get("display_name", handle.lstrip("@")),
        profile_url=payload.get("profile_url", ""),
        bio=payload.get("bio", ""),
        follower_count=int(payload.get("follower_count") or 0),
        avg_views=int(payload.get("avg_views") or 0),
        avg_likes=int(payload.get("avg_likes") or 0),
        engagement_notes=payload.get("engagement_notes", ""),
        categories=_split_list(payload.get("categories", [])),
        hashtags_used=_split_list(payload.get("hashtags_used", [])),
        recent_video_urls=_split_list(payload.get("recent_video_urls", [])),
        recent_video_summaries=_split_list(payload.get("recent_video_summaries", [])),
        email_or_contact=payload.get("email_or_contact", ""),
        region=payload.get("region", ""),
        language=payload.get("language", "en"),
        fit_status=payload.get("fit_status", "new"),
        source=payload.get("source", "manual_import"),
    )


def build_content_sample_from_manual_import(payload: dict) -> CreatorContentSample:
    return CreatorContentSample(
        id=payload.get("id") or stable_id("content", payload.get("creator_id"), payload.get("video_url")),
        creator_id=payload["creator_id"],
        video_url=payload.get("video_url", ""),
        title_or_caption=payload.get("title_or_caption", ""),
        transcript_or_summary=payload.get("transcript_or_summary", ""),
        hashtags=_split_list(payload.get("hashtags", [])),
        topics=_split_list(payload.get("topics", [])),
        format=payload.get("format", "other"),
        views=int(payload.get("views") or 0),
        likes=int(payload.get("likes") or 0),
        comments_count=int(payload.get("comments_count") or 0),
        posted_at=payload.get("posted_at", ""),
        notes=payload.get("notes", ""),
    )


def _split_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split("|") if item.strip()]

