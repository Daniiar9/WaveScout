from __future__ import annotations

from dataclasses import dataclass, field

from app.models.creator_candidate import CreatorCandidate
from app.models.creator_proposal import CreatorProposal
from app.models.trend_wave import TrendWave


@dataclass
class OutreachPacket:
    id: str
    creator_intelligence_packet_id: str
    creator: CreatorCandidate
    wave: TrendWave
    score: int
    fit_level: str
    best_angle: str
    proposal: CreatorProposal
    notion_payload: dict
    approval_required: bool = True
    send_allowed: bool = False
    status: str = "draft_review_required"
    evidence: list[str] = field(default_factory=list)

