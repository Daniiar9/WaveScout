from __future__ import annotations

from app.models import DiscoveryCandidate, DiscoveryCandidateNormalized
from app.services.text import normalize_handle


def normalize_discovery_candidate(raw_candidate: DiscoveryCandidate | dict) -> DiscoveryCandidateNormalized:
    data = raw_candidate if isinstance(raw_candidate, dict) else raw_candidate.__dict__
    handle = normalize_handle(str(data.get("handle", "")))
    profile_url = str(data.get("profile_url", "") or (f"https://www.tiktok.com/{handle}" if handle else ""))
    return DiscoveryCandidateNormalized(
        handle=handle,
        display_name=str(data.get("display_name", "") or handle.lstrip("@")),
        profile_url=profile_url,
        platform=str(data.get("platform", "tiktok") or "tiktok"),
        bio=str(data.get("bio", "") or data.get("raw_snippet", "")),
        matched_query=str(data.get("matched_query", "")),
        matched_wave=str(data.get("matched_wave", "")),
        matched_hashtags=list(data.get("matched_hashtags", []) or []),
        source_provider=str(data.get("source_provider", "") or data.get("source", "")),
        source_confidence=float(data.get("source_confidence", data.get("confidence", 0.0)) or 0.0),
        reason_found=str(data.get("reason_found", "")),
        raw_snippet=str(data.get("raw_snippet", "")),
        requires_manual_review=bool(data.get("requires_manual_review", True)),
    )

