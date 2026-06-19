from __future__ import annotations

import argparse

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from app.models.common import to_plain_dict
from app.services.outreach_packet_builder import build_creator_intelligence_packet, render_creator_packet_markdown
from app.services.storage import LocalJSONStorage


def build_packet(creator_handle: str, wave_name: str, product_context: str = DEFAULT_PRODUCT_CONTEXT):
    storage = LocalJSONStorage()
    creator = storage.find_creator(creator_handle)
    wave = storage.find_wave(wave_name)
    if not creator:
        raise SystemExit(f"Creator not found in local data: {creator_handle}")
    if not wave:
        raise SystemExit(f"Wave not found in local data: {wave_name}")
    return build_creator_intelligence_packet(
        product_context,
        wave,
        creator,
        storage.content_for_creator(creator.id),
        storage.comments_for_creator(creator.id),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build one creator intelligence packet.")
    parser.add_argument("--creator-handle", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--out", default="")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()
    packet = build_packet(args.creator_handle, args.wave)
    if args.format == "json":
        import json

        output = json.dumps(to_plain_dict(packet), indent=2, sort_keys=True)
    else:
        output = render_creator_packet_markdown(packet)
    if args.out:
        from pathlib import Path

        Path(args.out).write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()

