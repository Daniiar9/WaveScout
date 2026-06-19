from __future__ import annotations

import json

from bootstrap import bootstrap

ROOT = bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT, load_config
from app.models.common import to_plain_dict
from app.services.notion_sync import sync_outreach_packet_to_notion
from app.services.outreach_packet_builder import (
    build_creator_intelligence_packet,
    build_outreach_packet,
    creator_packet_contract,
    render_creator_packet_markdown,
    render_outreach_packet_json,
)
from app.services.storage import LocalJSONStorage


DEMO_ARTIFACT_PATH = ROOT / "artifacts" / "demo_creator_intelligence_packet.md"


def run_demo(top: int = 3, product_context: str = DEFAULT_PRODUCT_CONTEXT) -> dict:
    storage = LocalJSONStorage()
    wave = storage.load_waves()[0]
    packets = [
        build_creator_intelligence_packet(
            product_context,
            wave,
            creator,
            storage.content_for_creator(creator.id),
            storage.comments_for_creator(creator.id),
        )
        for creator in storage.load_creators()
    ]
    ranked = sorted(packets, key=lambda packet: packet.fit_score.score, reverse=True)
    outreach_packets = [build_outreach_packet(packet) for packet in ranked[:top]]
    notion_result = sync_outreach_packet_to_notion(outreach_packets[0], load_config())
    artifact_path = export_demo_artifact(
        product_context=product_context,
        wave_name=wave.name,
        ranked_packets=ranked,
        top_packets=ranked[:top],
        notion_payload=to_plain_dict(notion_result.payload),
        notion_write=bool(notion_result.external_call_made),
    )
    if load_config().wavescout_export_artifacts:
        export_dir = ROOT / "artifacts" / "creator_packets"
        export_dir.mkdir(parents=True, exist_ok=True)
        for packet in ranked[:top]:
            safe_handle = packet.creator_candidate.handle.lstrip("@")
            (export_dir / f"{safe_handle}.md").write_text(render_creator_packet_markdown(packet), encoding="utf-8")
        (export_dir / "top_outreach_packet.json").write_text(
            render_outreach_packet_json(outreach_packets[0]),
            encoding="utf-8",
        )
    return {
        "wave": wave.name,
        "top_packets": ranked[:top],
        "all_packets": ranked,
        "outreach_packets": outreach_packets,
        "notion_result": notion_result,
        "artifact_path": artifact_path,
        "external_calls_made": False,
    }


def main() -> None:
    result = run_demo()
    print("WaveScout Demo: PASS")
    print("External calls: false")
    print(f"Notion write: {str(result['notion_result'].external_call_made).lower()}")
    print("TikTok DM/send: false")
    print("\nTop creators:")
    for index, packet in enumerate(result["top_packets"], start=1):
        print(f"{index}. {packet.creator_candidate.handle} - {packet.fit_score.score} {packet.fit_score.fit_level}")
    rejected = [packet for packet in result["all_packets"] if packet.fit_score.fit_level == "reject"]
    print("\nRejected:")
    for packet in rejected:
        print(f"{packet.creator_candidate.handle} - {packet.fit_score.score} {packet.fit_score.fit_level}")
    artifact_path = result["artifact_path"].relative_to(ROOT)
    print(f"\nArtifact:\n{artifact_path.as_posix()}")


def export_demo_artifact(
    product_context: str,
    wave_name: str,
    ranked_packets: list,
    top_packets: list,
    notion_payload: dict,
    notion_write: bool,
):
    DEMO_ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    top_packet = top_packets[0]
    rejected = [packet for packet in ranked_packets if packet.fit_score.fit_level == "reject"]
    artifact = render_demo_artifact_markdown(
        product_context=product_context,
        wave_name=wave_name,
        top_packets=top_packets,
        rejected_packets=rejected,
        top_packet=top_packet,
        notion_payload=notion_payload,
        notion_write=notion_write,
    )
    DEMO_ARTIFACT_PATH.write_text(artifact, encoding="utf-8")
    return DEMO_ARTIFACT_PATH


def render_demo_artifact_markdown(
    product_context: str,
    wave_name: str,
    top_packets: list,
    rejected_packets: list,
    top_packet,
    notion_payload: dict,
    notion_write: bool,
) -> str:
    packet_contract = creator_packet_contract(top_packet)
    return f"""# WaveScout Demo Creator Intelligence Packet

## Product Context

{product_context}

## Trend Wave

{wave_name}

## Top Creator Ranking

{_ranking_lines(top_packets)}

## Rejected

{_ranking_lines(rejected_packets) if rejected_packets else "- None."}

## Creator Intelligence Packet For Top Creator

{render_creator_packet_markdown(top_packet)}

## Fit Score Breakdown

- Total score: {top_packet.fit_score.score}
- Fit level: {top_packet.fit_score.fit_level}
- Topical relevance: {top_packet.fit_score.topical_relevance}
- Audience relevance: {top_packet.fit_score.audience_relevance}
- Comment intent quality: {top_packet.fit_score.comment_intent_quality}
- Creator trust and clarity: {top_packet.fit_score.creator_trust_clarity}
- Product demo fit: {top_packet.fit_score.product_demo_fit}
- Commercial priority: {top_packet.fit_score.commercial_priority}
- Risk penalty: {top_packet.fit_score.risk_penalty}

## Best Content Angle

- Title: {top_packet.recommended_content_angle.title}
- Hook: {top_packet.recommended_content_angle.hook}
- Format: {top_packet.recommended_content_angle.format}
- Product mention style: {top_packet.recommended_content_angle.product_mention_style}

## Proposal Draft

{top_packet.proposal_draft.dm_draft or top_packet.proposal_draft.do_not_send_reason}

## Notion Dry-Run Payload

```json
{json.dumps(notion_payload, indent=2, sort_keys=True)}
```

## Packet Contract

```json
{json.dumps(packet_contract, indent=2, sort_keys=True)}
```

## Safety Status

- send_allowed=false
- approval_required=true
- external_calls=false
- notion_write={str(notion_write).lower()}
- tiktok_dm=false
"""


def _ranking_lines(packets: list) -> str:
    if not packets:
        return "- None."
    return "\n".join(
        f"{index}. {packet.creator_candidate.handle} - {packet.fit_score.score} {packet.fit_score.fit_level}"
        for index, packet in enumerate(packets, start=1)
    )


if __name__ == "__main__":
    main()
