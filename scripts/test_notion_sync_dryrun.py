from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT, load_config
from app.services.notion_sync import sync_outreach_packet_to_notion
from app.services.outreach_packet_builder import build_creator_intelligence_packet, build_outreach_packet
from app.services.storage import LocalJSONStorage


def main() -> None:
    storage = LocalJSONStorage()
    creator = storage.find_creator("@agentbuilderdaily")
    wave = storage.find_wave("Talk to your apps")
    assert creator and wave
    packet = build_creator_intelligence_packet(
        DEFAULT_PRODUCT_CONTEXT,
        wave,
        creator,
        storage.content_for_creator(creator.id),
        storage.comments_for_creator(creator.id),
    )
    outreach = build_outreach_packet(packet)
    result = sync_outreach_packet_to_notion(outreach, load_config())
    assert result.ok is True
    assert result.dry_run is True
    assert result.external_call_made is False
    assert result.payload["Send Allowed"] is False
    assert result.missing_database_ids
    print("test_notion_sync_dryrun passed")


if __name__ == "__main__":
    main()

