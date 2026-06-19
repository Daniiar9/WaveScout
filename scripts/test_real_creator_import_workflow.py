from __future__ import annotations

import csv
import tempfile
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from scripts.export_creator_packets import export_creator_packets
from scripts.import_comments_csv import import_csv as import_comments_csv
from scripts.import_content_samples_csv import import_csv as import_content_csv
from scripts.import_creators_csv import import_csv as import_creators_csv
from scripts.score_imported_creators import score_imported_creators


def main() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        creators_csv = root / "creators.csv"
        content_csv = root / "content.csv"
        comments_csv = root / "comments.csv"
        creators_json = root / "imported_creators.json"
        content_json = root / "imported_content_samples.json"
        comments_json = root / "imported_comments.json"
        ranking_md = root / "rankings.md"
        packet_dir = root / "packets"

        _write_csv(
            creators_csv,
            [
                "handle",
                "display_name",
                "profile_url",
                "bio",
                "follower_count",
                "avg_views",
                "avg_likes",
                "categories",
                "hashtags_used",
                "email_or_contact",
                "region",
                "language",
                "source",
                "notes",
            ],
            [
                [
                    "agentmanual",
                    "Agent Manual",
                    "https://www.tiktok.com/@agentmanual",
                    "AI agent demos for founders and RevOps teams using Slack, Notion, and CRM workflows.",
                    "9000",
                    "14000",
                    "700",
                    "AI agents; RevOps; founder tools",
                    "#AIAgents; #Automation",
                    "agentmanual@example.com",
                    "US",
                    "en",
                    "test",
                    "Strong fake candidate",
                ],
                [
                    "@broadtipsmanual",
                    "Broad Tips Manual",
                    "https://www.tiktok.com/@broadtipsmanual",
                    "General viral ChatGPT tips.",
                    "100000",
                    "80000",
                    "4000",
                    "ChatGPT tips; AI tourists",
                    "#ChatGPT; #AITips",
                    "broadtipsmanual@example.com",
                    "US",
                    "en",
                    "test",
                    "Low intent fake candidate",
                ],
            ],
        )
        _write_csv(
            content_csv,
            [
                "creator_handle",
                "video_url",
                "title_or_caption",
                "transcript_or_summary",
                "hashtags",
                "topics",
                "format",
                "views",
                "likes",
                "comments_count",
                "posted_at",
                "notes",
            ],
            [
                [
                    "@agentmanual",
                    "https://www.tiktok.com/@agentmanual/video/1",
                    "I asked Slack and Notion one question",
                    "Demo of an AI agent reading CRM notes, Slack updates, and Notion docs.",
                    "#AIAgents; #RevOps",
                    "AI agents; Slack; Notion; CRM; workflow automation",
                    "demo",
                    "15000",
                    "900",
                    "25",
                    "2026-06-01",
                    "Relevant fake sample",
                ],
                [
                    "@broadtipsmanual",
                    "https://www.tiktok.com/@broadtipsmanual/video/1",
                    "Three viral ChatGPT prompts",
                    "Generic prompt tips with little workflow specificity.",
                    "#ChatGPT; #AITips",
                    "ChatGPT tips; prompts",
                    "hot_take",
                    "90000",
                    "5000",
                    "80",
                    "2026-06-01",
                    "Broad fake sample",
                ],
            ],
        )
        _write_csv(
            comments_csv,
            ["creator_handle", "video_url", "comment_text", "notes"],
            [
                ["agentmanual", "https://www.tiktok.com/@agentmanual/video/1", "Can this connect to Notion?", "Tool intent"],
                ["agentmanual", "https://www.tiktok.com/@agentmanual/video/1", "Does it work with Slack?", "Tool intent"],
                ["agentmanual", "https://www.tiktok.com/@agentmanual/video/1", "I need this for my CRM.", "Use case"],
                ["agentmanual", "https://www.tiktok.com/@agentmanual/video/1", "Can you make a tutorial?", "Tutorial demand"],
                ["@broadtipsmanual", "https://www.tiktok.com/@broadtipsmanual/video/1", "AI is crazy", "Low quality"],
                ["@broadtipsmanual", "https://www.tiktok.com/@broadtipsmanual/video/1", "first", "Low quality"],
            ],
        )

        creators, skipped_creators = import_creators_csv(str(creators_csv), str(creators_json))
        content, skipped_content = import_content_csv(str(content_csv), str(content_json))
        comments, skipped_comments = import_comments_csv(str(comments_csv), str(comments_json))

        assert len(creators) == 2
        assert creators[0].handle == "@agentmanual"
        assert len(content) == 2
        assert len(comments) == 6
        assert skipped_creators == skipped_content == skipped_comments == 0

        score_result = score_imported_creators(
            str(creators_json),
            str(content_json),
            str(comments_json),
            "Talk to your apps",
            DEFAULT_PRODUCT_CONTEXT,
            5,
            str(ranking_md),
        )
        assert ranking_md.exists()
        assert "WaveScout Imported Creator Ranking" in ranking_md.read_text(encoding="utf-8")
        assert score_result["external_calls_made"] is False

        export_result = export_creator_packets(
            str(creators_json),
            str(content_json),
            str(comments_json),
            "Talk to your apps",
            DEFAULT_PRODUCT_CONTEXT,
            str(packet_dir),
            10,
        )
        assert export_result["exported"]
        first_packet = export_result["exported"][0].read_text(encoding="utf-8")
        assert "## Outreach Decision" in first_packet
        assert "send_allowed=false" in first_packet
        assert "approval_required=true" in first_packet
        assert "external_calls=false" in first_packet
        assert "Do not send automatically: true" in first_packet

        top_packet = score_result["top_packets"][0]
        assert top_packet.proposal_draft.send_allowed is False
        assert top_packet.proposal_draft.approval_required is True
        assert score_result["external_calls_made"] is False
        assert export_result["external_calls_made"] is False

    print("test_real_creator_import_workflow passed")


def _write_csv(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


if __name__ == "__main__":
    main()

