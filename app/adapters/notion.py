from __future__ import annotations

from app.config import AppConfig, load_config
from app.models import CreatorIntelligencePacket, NotionSyncResult, OutreachPacket
from app.models.common import to_plain_dict


def build_creator_packet_payload(packet: CreatorIntelligencePacket) -> dict:
    return {
        "Creator": packet.creator_candidate.handle,
        "Wave": packet.trend_wave.name,
        "Fit Score": packet.fit_score.score,
        "Recommended Angle": packet.recommended_content_angle.title,
        "Proposal Draft": packet.proposal_draft.dm_draft,
        "Risks": "; ".join(packet.risks),
        "Next Safe Action": packet.next_safe_action,
        "Approval Required": packet.approval_required,
        "Send Allowed": packet.send_allowed,
        "Status": "draft_review_required",
        "Evidence": packet.evidence,
    }


def build_outreach_payload(outreach_packet: OutreachPacket) -> dict:
    return {
        "Creator": outreach_packet.creator.handle,
        "Wave": outreach_packet.wave.name,
        "Fit Score": outreach_packet.score,
        "Fit Level": outreach_packet.fit_level,
        "Best Angle": outreach_packet.best_angle,
        "Proposal Draft": outreach_packet.proposal.dm_draft,
        "Approval Required": outreach_packet.approval_required,
        "Send Allowed": outreach_packet.send_allowed,
        "Status": outreach_packet.status,
        "Evidence": outreach_packet.evidence,
    }


def dry_run_or_sync(target: str, payload: dict, config: AppConfig | None = None) -> NotionSyncResult:
    config = config or load_config()
    missing = _missing_database_ids(target, config)
    should_write = (
        config.notion_sync_confirm
        and config.wavescout_allow_external_calls
        and bool(config.notion_api_key)
        and not missing
    )
    if not should_write:
        reason = "Dry run only. No Notion write attempted."
        if missing:
            reason += f" Missing database ids: {', '.join(missing)}."
        return NotionSyncResult(
            ok=True,
            dry_run=True,
            target=target,
            payload=to_plain_dict(payload),
            message=reason,
            external_call_made=False,
            missing_database_ids=missing,
        )
    return NotionSyncResult(
        ok=False,
        dry_run=True,
        target=target,
        payload=to_plain_dict(payload),
        message="Live Notion writes are intentionally not implemented in V0.",
        external_call_made=False,
        missing_database_ids=[],
    )


def _missing_database_ids(target: str, config: AppConfig) -> list[str]:
    missing: list[str] = []
    if target in {"creator", "creator_packet"} and not config.notion_tiktok_creators_database_id:
        missing.append("NOTION_TIKTOK_CREATORS_DATABASE_ID")
    if target in {"wave"} and not config.notion_tiktok_waves_database_id:
        missing.append("NOTION_TIKTOK_WAVES_DATABASE_ID")
    if target in {"outreach", "creator_packet"} and not config.notion_tiktok_outreach_database_id:
        missing.append("NOTION_TIKTOK_OUTREACH_DATABASE_ID")
    return missing

