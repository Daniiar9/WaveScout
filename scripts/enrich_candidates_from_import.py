from __future__ import annotations

import argparse
import json
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from app.models import CreatorCandidate, CreatorContentSample
from app.services.growth_engine import run_growth_engine
from app.services.outreach_packet_builder import render_creator_packet_markdown
from app.services.storage import coerce_dataclass
from app.services.text import normalize_handle


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich discovery candidates with imported creator/content/comment data.")
    parser.add_argument("--candidates", default="artifacts/discovery_candidates.json")
    parser.add_argument("--creators", default="data/imported_creators.json")
    parser.add_argument("--content", default="data/imported_content_samples.json")
    parser.add_argument("--comments", default="data/imported_comments.json")
    parser.add_argument("--product-text", default=DEFAULT_PRODUCT_CONTEXT)
    parser.add_argument("--wave", default="Talk to your apps")
    parser.add_argument("--out", default="artifacts/enriched_creator_packets.md")
    args = parser.parse_args()
    matched_creators = _matched_creators(args.candidates, args.creators)
    growth_brief = run_growth_engine(
        product_text=args.product_text,
        imported_creators=matched_creators,
        imported_content=args.content,
        imported_comments=args.comments,
        top_creators=len(matched_creators) or 5,
    )
    output = _render_enriched_packets(growth_brief)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")
    print("WaveScout Candidate Enrichment: PASS")
    print("External calls: false")
    print("TikTok scraping: false")
    print("TikTok DM/send: false")
    print(f"matched creators: {len(matched_creators)}")
    print(f"packets: {len(growth_brief.top_creator_packets)}")
    print(f"Artifact:\n{out_path.as_posix()}")


def _matched_creators(candidates_path: str, creators_path: str) -> list[CreatorCandidate]:
    creators = _load_creators(creators_path)
    candidate_path = Path(candidates_path)
    if not candidate_path.exists():
        return creators
    candidates = json.loads(candidate_path.read_text(encoding="utf-8"))
    handles = {normalize_handle(item.get("handle", "")) for item in candidates}
    return [creator for creator in creators if creator.handle in handles] or creators


def _load_creators(path: str) -> list[CreatorCandidate]:
    input_path = Path(path)
    if not input_path.exists():
        return []
    return [coerce_dataclass(CreatorCandidate, item) for item in json.loads(input_path.read_text(encoding="utf-8"))]


def _render_enriched_packets(growth_brief) -> str:
    packets = "\n\n".join(render_creator_packet_markdown(packet) for packet in growth_brief.top_creator_packets)
    return f"""# Enriched Creator Packets

## Safety Status
- external_calls=false
- tiktok_scraping=false
- tiktok_dm_send=false
- send_allowed=false
- approval_required=true

## Packet Summary
- Packets built: {len(growth_brief.top_creator_packets)}
- Missing data: {", ".join(growth_brief.missing_data) if growth_brief.missing_data else "None"}

{packets or "No packets built. Import matching creator content and comments first."}
"""


if __name__ == "__main__":
    main()

