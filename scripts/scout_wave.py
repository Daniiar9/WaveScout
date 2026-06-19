from __future__ import annotations

import argparse
import json
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from app.models.common import to_plain_dict
from app.services.outreach_packet_builder import build_creator_intelligence_packet
from app.services.storage import LocalJSONStorage


def scout_wave(wave_name: str, product: str, top: int = 3) -> dict:
    storage = LocalJSONStorage()
    wave = storage.find_wave(wave_name)
    if not wave:
        raise SystemExit(f"Wave not found in local data: {wave_name}")
    packets = [
        build_creator_intelligence_packet(
            product,
            wave,
            creator,
            storage.content_for_creator(creator.id),
            storage.comments_for_creator(creator.id),
        )
        for creator in storage.load_creators()
    ]
    ranked = sorted(packets, key=lambda packet: packet.fit_score.score, reverse=True)
    return {
        "wave": wave.name,
        "top": to_plain_dict(ranked[:top]),
        "external_calls_made": False,
        "send_allowed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank local creator candidates for a trend wave.")
    parser.add_argument("--wave", required=True)
    parser.add_argument("--product", default=DEFAULT_PRODUCT_CONTEXT)
    parser.add_argument("--creators", default="", help="Reserved for future JSON imports; demo data is used in V0.")
    parser.add_argument("--comments", default="", help="Reserved for future JSON imports; demo data is used in V0.")
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--out", default="")
    parser.add_argument("--notion-dry-run", action="store_true")
    args = parser.parse_args()
    result = scout_wave(args.wave, args.product, args.top)
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

