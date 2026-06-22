from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.models import CreatorContentSample
from app.services.owned_tiktok_analysis import analyze_owned_tiktok_profile, render_owned_tiktok_profile_markdown


def main() -> None:
    content = [
        CreatorContentSample(
            id="owned_1",
            creator_id="owned",
            title_or_caption="I asked Slack and Notion one question",
            transcript_or_summary="Demo showing an AI workspace connecting Slack, Notion, and CRM context.",
            topics=["AI workspace", "Slack", "Notion", "CRM"],
            format="demo",
        )
    ]
    comments = [
        "Can this connect to Notion?",
        "Does it work with Slack?",
        "I need this for my CRM.",
    ]
    profile = analyze_owned_tiktok_profile("@demoapp", content, comments)
    assert profile.handle == "@demoapp"
    assert "AI workspace" in profile.content_themes
    assert profile.audience_questions
    assert "demo" in profile.top_formats
    assert profile.confidence >= 0.7
    assert "Owned TikTok Account Intelligence" in render_owned_tiktok_profile_markdown(profile)
    print("test_owned_tiktok_analysis passed")


if __name__ == "__main__":
    main()

