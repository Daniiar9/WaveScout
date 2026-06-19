from __future__ import annotations

import json

from app.adapters.notion import build_outreach_payload
from app.models import (
    CreatorCandidate,
    CreatorContentSample,
    CreatorIntelligencePacket,
    OutreachPacket,
    TrendWave,
)
from app.models.common import to_plain_dict
from app.services.audience_analysis import infer_audience_profile
from app.services.comment_intelligence import extract_comment_signals, summarize_comment_intelligence
from app.services.content_angle_generator import generate_content_angles
from app.services.creator_content_analysis import summarize_creator_content
from app.services.creator_scoring import score_creator_for_wave
from app.services.proposal_generator import generate_creator_proposal
from app.services.text import stable_id


def build_creator_intelligence_packet(
    product_context: str,
    trend_wave: TrendWave,
    creator: CreatorCandidate,
    content_samples: list[CreatorContentSample],
    comments: list[str | dict],
) -> CreatorIntelligencePacket:
    comment_signals = extract_comment_signals(comments, creator.id)
    comment_summary = summarize_comment_intelligence(comment_signals)
    content_summary = summarize_creator_content(creator, content_samples)
    audience_profile = infer_audience_profile(creator, content_samples, comment_signals, product_context)
    fit_score = score_creator_for_wave(
        creator=creator,
        trend_wave=trend_wave,
        content_samples=content_samples,
        comment_signals=comment_signals,
        product_context=product_context,
        audience_profile=audience_profile,
        content_summary=content_summary,
    )
    angles = generate_content_angles(
        product_context=product_context,
        trend_wave=trend_wave,
        creator=creator,
        content_summary=content_summary,
        audience_profile=audience_profile,
        comment_intelligence_summary=comment_summary,
    )
    recommended_angle = angles[0]
    proposal = generate_creator_proposal(creator, trend_wave, fit_score, recommended_angle, product_context)
    missing_data = _missing_data(creator, content_samples, comments)
    next_safe_action = _next_safe_action(fit_score.fit_level, missing_data)
    packet = CreatorIntelligencePacket(
        id=stable_id("packet", trend_wave.id, creator.id),
        trend_wave=trend_wave,
        creator_candidate=creator,
        content_summary=content_summary,
        audience_profile=audience_profile,
        comment_intelligence_summary=comment_summary,
        fit_score=fit_score,
        recommended_content_angle=recommended_angle,
        proposal_draft=proposal,
        risks=fit_score.risks + recommended_angle.avoid_saying,
        missing_data=missing_data,
        evidence=_evidence(content_samples, comments, comment_summary),
        next_safe_action=next_safe_action,
        approval_required=True,
        send_allowed=False,
    )
    return packet


def build_outreach_packet(packet: CreatorIntelligencePacket) -> OutreachPacket:
    outreach = OutreachPacket(
        id=stable_id("outreach", packet.id),
        creator_intelligence_packet_id=packet.id,
        creator=packet.creator_candidate,
        wave=packet.trend_wave,
        score=packet.fit_score.score,
        fit_level=packet.fit_score.fit_level,
        best_angle=packet.recommended_content_angle.title,
        proposal=packet.proposal_draft,
        notion_payload={},
        approval_required=True,
        send_allowed=False,
        status="draft_review_required" if packet.fit_score.fit_level in {"high", "medium"} else "do_not_contact",
        evidence=packet.evidence,
    )
    outreach.notion_payload = build_outreach_payload(outreach)
    return outreach


def render_creator_packet_markdown(packet: CreatorIntelligencePacket) -> str:
    proposal = packet.proposal_draft.dm_draft or packet.proposal_draft.do_not_send_reason
    return f"""# Creator Intelligence Packet: {packet.creator_candidate.handle}

## Summary
- Creator: {packet.creator_candidate.display_name} ({packet.creator_candidate.handle})
- Trend wave: {packet.trend_wave.name}
- Fit score: {packet.fit_score.score} ({packet.fit_score.fit_level})
- Send allowed: {str(packet.send_allowed).lower()}
- Approval required: {str(packet.approval_required).lower()}

## Why This Creator
{_bullets(packet.fit_score.reasons)}

## Why This Trend
{packet.trend_wave.product_relevance}

## Content Themes
{_bullets(packet.content_summary.get("themes", []))}

## Audience Profile
- Segments: {", ".join(packet.audience_profile.likely_audience_segments)}
- Quality: {packet.audience_profile.audience_quality_level}
- Buyer intent: {packet.audience_profile.buyer_intent_summary}

## Comment Intelligence
- Buyer intent count: {packet.comment_intelligence_summary.get("buyer_intent_count", 0)}
- Top intents: {", ".join(packet.comment_intelligence_summary.get("top_intent_types", []))}
- Tool mentions: {", ".join(packet.comment_intelligence_summary.get("tool_mentions", [])) or "None"}
- Summary: {packet.comment_intelligence_summary.get("summary", "")}

## Recommended Angle
{packet.recommended_content_angle.title}

{packet.recommended_content_angle.short_script}

## Proposal Draft
{proposal}

## Risks And Avoid Saying
{_bullets(packet.risks)}

## Missing Data
{_bullets(packet.missing_data) if packet.missing_data else "- None for V0 demo review."}

## Evidence
{_bullets(packet.evidence)}

## Next Safe Action
{packet.next_safe_action}
"""


def render_outreach_packet_json(packet: OutreachPacket) -> str:
    return json.dumps(to_plain_dict(packet), indent=2, sort_keys=True)


def creator_packet_contract(packet: CreatorIntelligencePacket) -> dict:
    return {
        "id": packet.id,
        "creator": to_plain_dict(packet.creator_candidate),
        "wave": to_plain_dict(packet.trend_wave),
        "score": packet.fit_score.score,
        "fit_level": packet.fit_score.fit_level,
        "audience_profile": to_plain_dict(packet.audience_profile),
        "comment_intelligence": packet.comment_intelligence_summary,
        "content_angle": to_plain_dict(packet.recommended_content_angle),
        "proposal": to_plain_dict(packet.proposal_draft),
        "risks": packet.risks,
        "next_safe_action": packet.next_safe_action,
        "approval_required": True,
        "send_allowed": False,
        "evidence": packet.evidence,
    }


def _missing_data(
    creator: CreatorCandidate,
    content_samples: list[CreatorContentSample],
    comments: list[str | dict],
) -> list[str]:
    missing: list[str] = []
    if not creator.email_or_contact:
        missing.append("No creator contact imported.")
    if not content_samples:
        missing.append("No content samples imported.")
    if not comments:
        missing.append("No comment samples imported.")
    if not creator.region:
        missing.append("Creator region unknown.")
    return missing


def _next_safe_action(fit_level: str, missing_data: list[str]) -> str:
    if fit_level == "high" and not missing_data:
        return "Human review of packet and proposal draft before any manual outreach."
    if fit_level in {"high", "medium"}:
        return "Fill missing data, then human-review the draft before any manual outreach."
    return "Do not contact. Import stronger evidence or archive."


def _evidence(content_samples: list[CreatorContentSample], comments: list[str | dict], comment_summary: dict) -> list[str]:
    evidence: list[str] = []
    for sample in content_samples[:3]:
        label = sample.title_or_caption or sample.video_url or sample.id
        evidence.append(f"Content sample: {label}")
    for question in comment_summary.get("common_questions", [])[:3]:
        evidence.append(f"Audience question: {question}")
    for pain in comment_summary.get("common_pains", [])[:3]:
        evidence.append(f"Audience pain/use case: {pain}")
    if comments and not evidence:
        evidence.append(f"{len(comments)} comments imported for manual analysis.")
    return evidence


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)
