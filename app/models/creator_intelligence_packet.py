from __future__ import annotations

from dataclasses import dataclass, field

from app.models.audience_profile import AudienceProfile
from app.models.common import utc_now_iso
from app.models.content_angle import ContentAngle
from app.models.creator_candidate import CreatorCandidate
from app.models.creator_fit_score import CreatorFitScore
from app.models.creator_proposal import CreatorProposal
from app.models.trend_wave import TrendWave


@dataclass
class CreatorIntelligencePacket:
    id: str
    trend_wave: TrendWave
    creator_candidate: CreatorCandidate
    content_summary: dict
    audience_profile: AudienceProfile
    comment_intelligence_summary: dict
    fit_score: CreatorFitScore
    recommended_content_angle: ContentAngle
    proposal_draft: CreatorProposal
    risks: list[str] = field(default_factory=list)
    missing_data: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    next_safe_action: str = "Human review before any outreach."
    approval_required: bool = True
    send_allowed: bool = False
    created_at: str = field(default_factory=utc_now_iso)

