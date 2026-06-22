from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.models import CreatorCandidate, CreatorContentSample
from app.services.growth_engine import run_growth_engine

PRODUCT_TEXT = "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows."


def main() -> None:
    brief = run_growth_engine(product_text=PRODUCT_TEXT)
    assert brief.product_brief.category == "AI workspace / connected SaaS stack"
    assert brief.safety_status["external_calls"] is False
    assert brief.safety_status["send_allowed"] is False
    assert brief.missing_data

    creator = CreatorCandidate(
        id="creator_fake",
        handle="@fakebuilder",
        display_name="Fake Builder",
        bio="AI agents and RevOps workflow demos using Slack and Notion.",
        categories=["AI agents", "RevOps"],
        hashtags_used=["#AIAgents", "#RevOps"],
        email_or_contact="fake@example.com",
        region="US",
    )
    content = [
        CreatorContentSample(
            id="content_fake",
            creator_id="creator_fake",
            title_or_caption="I asked Slack and Notion one question",
            transcript_or_summary="Demo of connected SaaS stack workflow automation.",
            topics=["AI workspace", "Slack", "Notion", "CRM"],
            format="demo",
        )
    ]
    comments = [
        {"creator_id": "creator_fake", "comment_text": "Can this connect to Notion?"},
        {"creator_id": "creator_fake", "comment_text": "Does it work with Slack?"},
        {"creator_id": "creator_fake", "comment_text": "I need this for my CRM."},
    ]
    enriched = run_growth_engine(
        product_text=PRODUCT_TEXT,
        imported_creators=[creator],
        imported_content=content,
        imported_comments=comments,
    )
    assert enriched.top_creator_packets
    assert enriched.top_creator_packets[0].send_allowed is False
    assert enriched.top_creator_packets[0].approval_required is True
    assert enriched.discovery_summary["candidates_from_manual_import"] == 1
    print("test_growth_engine passed")


if __name__ == "__main__":
    main()

