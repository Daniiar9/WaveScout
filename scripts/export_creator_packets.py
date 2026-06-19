from __future__ import annotations

import argparse
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT, load_config
from app.models.common import to_plain_dict
from app.services.notion_sync import sync_outreach_packet_to_notion
from app.services.outreach_packet_builder import (
    build_outreach_packet,
    render_creator_packet_export_markdown,
)
from scripts.import_utils import safe_filename_for_handle
from scripts.score_imported_creators import load_imported_packets


def export_creator_packets(
    creators_path: str,
    content_path: str,
    comments_path: str,
    wave_name: str,
    product_context: str,
    out_dir: str,
    top: int,
    include_rejected: bool = False,
) -> dict:
    _wave, ranked_packets = load_imported_packets(creators_path, content_path, comments_path, wave_name, product_context)
    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    exportable = [
        packet
        for packet in ranked_packets
        if include_rejected or packet.fit_score.fit_level != "reject"
    ][:top]
    exported: list[Path] = []
    for packet in exportable:
        outreach = build_outreach_packet(packet)
        notion_result = sync_outreach_packet_to_notion(outreach, load_config())
        filename = safe_filename_for_handle(packet.creator_candidate.handle, "packet.md")
        output = output_dir / filename
        output.write_text(
            render_creator_packet_export_markdown(
                packet,
                notion_payload=to_plain_dict(notion_result.payload),
                notion_write=notion_result.external_call_made,
            ),
            encoding="utf-8",
        )
        exported.append(output)
    summary_path = output_dir / "summary.md"
    rejected = [packet for packet in ranked_packets if packet.fit_score.fit_level == "reject"]
    summary_path.write_text(_summary_markdown(exported, rejected, include_rejected), encoding="utf-8")
    return {
        "exported": exported,
        "summary": summary_path,
        "rejected": rejected,
        "external_calls_made": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export one markdown creator intelligence packet per imported creator.")
    parser.add_argument("--creators", default="data/imported_creators.json")
    parser.add_argument("--content", default="data/imported_content_samples.json")
    parser.add_argument("--comments", default="data/imported_comments.json")
    parser.add_argument("--wave", default="Talk to your apps")
    parser.add_argument("--product", default=DEFAULT_PRODUCT_CONTEXT)
    parser.add_argument("--out-dir", default="artifacts/creator_packets")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--include-rejected", action="store_true")
    args = parser.parse_args()
    result = export_creator_packets(
        args.creators,
        args.content,
        args.comments,
        args.wave,
        args.product,
        args.out_dir,
        args.top,
        args.include_rejected,
    )
    print("Creator packet export: PASS")
    print("External calls: false")
    print("Notion write: false")
    print("TikTok DM/send: false")
    print(f"exported packets: {len(result['exported'])}")
    print(f"summary: {result['summary'].as_posix()}")
    for path in result["exported"]:
        print(f"- {path.as_posix()}")


def _summary_markdown(exported: list[Path], rejected: list, include_rejected: bool) -> str:
    exported_lines = "\n".join(f"- {path.name}" for path in exported) if exported else "- None."
    rejected_lines = "\n".join(
        f"- {packet.creator_candidate.handle} - {packet.fit_score.score} {packet.fit_score.fit_level}"
        for packet in rejected
    ) or "- None."
    return f"""# Creator Packet Export Summary

## Exported Packets

{exported_lines}

## Rejected Creators

{rejected_lines}

Rejected creators are summarized here and not exported as full packets unless `--include-rejected` is passed.

include_rejected={str(include_rejected).lower()}

## Safety Status

- send_allowed=false
- approval_required=true
- external_calls=false
- notion_write=false
- tiktok_dm=false
"""


if __name__ == "__main__":
    main()

