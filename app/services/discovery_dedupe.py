from __future__ import annotations

from app.models import CreatorSearchStrategy, DiscoveryCandidateNormalized
from app.services.text import tokenize


def dedupe_discovery_candidates(candidates: list[DiscoveryCandidateNormalized]) -> list[DiscoveryCandidateNormalized]:
    seen: set[str] = set()
    deduped: list[DiscoveryCandidateNormalized] = []
    for candidate in candidates:
        key = candidate.handle.lower().lstrip("@") or candidate.profile_url.lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
    return deduped


def rank_discovery_candidates_initial(
    candidates: list[DiscoveryCandidateNormalized],
    strategy: CreatorSearchStrategy,
) -> list[DiscoveryCandidateNormalized]:
    keywords = set()
    for item in strategy.keywords + strategy.trend_waves + strategy.hashtags:
        keywords |= tokenize(item)

    def score(candidate: DiscoveryCandidateNormalized) -> float:
        text = " ".join(
            [
                candidate.handle,
                candidate.bio,
                candidate.raw_snippet,
                candidate.reason_found,
                " ".join(candidate.matched_hashtags),
            ]
        )
        overlap = len(tokenize(text) & keywords)
        return candidate.source_confidence + (overlap * 0.08)

    return sorted(candidates, key=score, reverse=True)

