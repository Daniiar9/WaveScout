from __future__ import annotations

from app.adapters.notion import build_creator_packet_payload, build_outreach_payload, dry_run_or_sync
from app.config import AppConfig, load_config
from app.models import CreatorIntelligencePacket, NotionSyncResult, OutreachPacket


def sync_creator_to_notion(
    packet: CreatorIntelligencePacket,
    config: AppConfig | None = None,
) -> NotionSyncResult:
    return dry_run_or_sync("creator_packet", build_creator_packet_payload(packet), config or load_config())


def sync_outreach_packet_to_notion(
    outreach_packet: OutreachPacket,
    config: AppConfig | None = None,
) -> NotionSyncResult:
    return dry_run_or_sync("outreach", build_outreach_payload(outreach_packet), config or load_config())

