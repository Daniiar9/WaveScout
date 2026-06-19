from __future__ import annotations

import argparse
import json
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from app.models import CreatorCandidate, CreatorContentSample
from app.services.outreach_packet_builder import (
    build_creator_intelligence_packet,
    render_creator_comparison_markdown,
)
from app.services.storage import LocalJSONStorage, coerce_dataclass


def load_imported_packets(
    creators_path: str,
    content_path: str,
    comments_path: str,
    wave_name: str,
    product_context: str,
):
    storage = LocalJSONStorage()
    wave = storage.find_wave(wave_name)
    if wave is None:
        raise SystemExit(f"Wave not found in local demo wave storage: {wave_name}")
    creators = [coerce_dataclass(CreatorCandidate, item) for item in _read_json(creators_path)]
    content_samples = [coerce_dataclass(CreatorContentSample, item) for item in _read_json(content_path)]
    comments = _read_json(comments_path)
    packets = []
    for creator in creators:
        creator_content = [sample for sample in content_samples if sample.creator_id == creator.id]
        creator_comments = [comment for comment in comments if comment.get("creator_id") == creator.id]
        packets.append(
            build_creator_intelligence_packet(
                product_context,
                wave,
                creator,
                creator_content,
                creator_comments,
            )
        )
    return wave, sorted(packets, key=lambda packet: packet.fit_score.score, reverse=True)


def score_imported_creators(
    creators_path: str,
    content_path: str,
    comments_path: str,
    wave_name: str,
    product_context: str,
    top: int,
    out_path: str,
) -> dict:
    wave, ranked_packets = load_imported_packets(creators_path, content_path, comments_path, wave_name, product_context)
    markdown = render_creator_comparison_markdown(product_context, wave, ranked_packets, top_count=top)
    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    top_packets = [packet for packet in ranked_packets if packet.fit_score.fit_level != "reject"][:top]
    rejected = [packet for packet in ranked_packets if packet.fit_score.fit_level == "reject"]
    return {
        "wave": wave,
        "ranked_packets": ranked_packets,
        "top_packets": top_packets,
        "rejected": rejected,
        "output": output,
        "external_calls_made": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score manually imported creators for a WaveScout trend wave.")
    parser.add_argument("--creators", default="data/imported_creators.json")
    parser.add_argument("--content", default="data/imported_content_samples.json")
    parser.add_argument("--comments", default="data/imported_comments.json")
    parser.add_argument("--wave", default="Talk to your apps")
    parser.add_argument("--product", default=DEFAULT_PRODUCT_CONTEXT)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--out", default="artifacts/imported_creator_rankings.md")
    args = parser.parse_args()
    result = score_imported_creators(
        args.creators,
        args.content,
        args.comments,
        args.wave,
        args.product,
        args.top,
        args.out,
    )
    print("Imported creator scoring: PASS")
    print("External calls: false")
    print("Notion write: false")
    print("TikTok DM/send: false")
    print("\nTop creators:")
    for index, packet in enumerate(result["top_packets"], start=1):
        print(f"{index}. {packet.creator_candidate.handle} - {packet.fit_score.score} {packet.fit_score.fit_level}")
    print("\nRejected:")
    if result["rejected"]:
        for packet in result["rejected"]:
            print(f"{packet.creator_candidate.handle} - {packet.fit_score.score} {packet.fit_score.fit_level}")
    else:
        print("None")
    print(f"\nArtifact:\n{result['output'].as_posix()}")


def _read_json(path: str) -> list:
    input_path = Path(path)
    if not input_path.exists():
        raise SystemExit(f"Missing input JSON: {path}")
    return json.loads(input_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

