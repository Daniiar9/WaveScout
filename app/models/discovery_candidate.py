from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DiscoveryCandidate:
    handle: str
    profile_url: str = ""
    source: str = "manual"
    matched_query: str = ""
    matched_wave: str = ""
    matched_hashtags: list[str] = field(default_factory=list)
    reason_found: str = ""
    raw_snippet: str = ""
    confidence: float = 0.0
    requires_manual_review: bool = True

