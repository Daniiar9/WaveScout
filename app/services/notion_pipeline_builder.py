from __future__ import annotations

from app.adapters.notion import build_creator_packet_payload, build_outreach_payload
from app.models import CreatorIntelligencePacket, GrowthBrief
from app.models.common import to_plain_dict
from app.services.outreach_packet_builder import build_outreach_packet


def build_growth_brief_notion_payload(growth_brief: GrowthBrief) -> dict:
    return {
        "Name": f"Growth Brief - {growth_brief.product_brief.product_name or growth_brief.product_brief.category}",
        "Product": growth_brief.product_brief.one_liner,
        "Category": growth_brief.product_brief.category,
        "Primary Waves": ", ".join(growth_brief.wave_map.primary_waves),
        "Top Candidates": ", ".join(candidate.handle for candidate in growth_brief.candidate_shortlist[:10]),
        "Top Creator Packets": ", ".join(packet.creator_candidate.handle for packet in growth_brief.top_creator_packets),
        "External Calls": growth_brief.safety_status.get("external_calls", False),
        "Send Allowed": growth_brief.safety_status.get("send_allowed", False),
        "Approval Required": growth_brief.safety_status.get("approval_required", True),
        "Next Safe Actions": "\n".join(growth_brief.next_safe_actions),
    }


def build_creator_pipeline_payload(packet: CreatorIntelligencePacket) -> dict:
    outreach = build_outreach_packet(packet)
    return {
        "creator_packet": build_creator_packet_payload(packet),
        "outreach_packet": build_outreach_payload(outreach),
        "send_allowed": False,
        "approval_required": True,
        "human_review_required": True,
    }


def build_notion_pipeline_payloads(
    growth_brief: GrowthBrief,
    packets: list[CreatorIntelligencePacket] | None = None,
) -> dict:
    packets = packets or growth_brief.top_creator_packets
    return {
        "dry_run": True,
        "notion_write": False,
        "growth_brief": build_growth_brief_notion_payload(growth_brief),
        "creator_pipeline": [build_creator_pipeline_payload(packet) for packet in packets],
    }


def render_notion_pipeline_markdown(payloads: dict) -> str:
    creator_count = len(payloads.get("creator_pipeline", []))
    return f"""# Notion Dry-Run Pipeline

- Dry run: {str(payloads.get("dry_run", True)).lower()}
- Notion write: {str(payloads.get("notion_write", False)).lower()}
- Creator payloads: {creator_count}

## Growth Brief Payload

```json
{to_plain_dict(payloads.get("growth_brief", {}))}
```

## Creator Pipeline Payloads

```json
{to_plain_dict(payloads.get("creator_pipeline", []))}
```
"""

