from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.mcp.tools import (
    TOOL_REGISTRY,
    build_tiktok_oauth_setup_instructions,
    check_tiktok_capabilities,
    get_tiktok_capability,
    tiktok_content_post_dry_run,
    tiktok_display_user_info_dry_run,
    tiktok_research_query_dry_run,
)


def main() -> None:
    expected_tools = {
        "check_tiktok_capabilities",
        "get_tiktok_capability",
        "build_tiktok_oauth_setup_instructions",
        "tiktok_display_user_info_dry_run",
        "tiktok_research_query_dry_run",
        "tiktok_content_post_dry_run",
    }
    assert expected_tools <= set(TOOL_REGISTRY)
    assert "tiktok_dm_send" not in TOOL_REGISTRY
    report = check_tiktok_capabilities()
    assert report["external_calls_made"] is False
    assert report["tiktok_scraping"] is False
    assert report["tiktok_dm_send"] is False
    dm = get_tiktok_capability("tiktok_dm_send")
    assert dm["capability"]["status"] == "blocked"
    instructions = build_tiktok_oauth_setup_instructions("user.info.basic,video.list")
    assert instructions["external_calls"] is False
    display = tiktok_display_user_info_dry_run()
    research = tiktok_research_query_dry_run({"keyword": "AI workspace"}, ["id"])
    post = tiktok_content_post_dry_run({"title": "draft only"})
    assert display["external_calls_made"] is False
    assert research["external_calls_made"] is False
    assert post["external_calls_made"] is False
    assert post["live_post_allowed"] is False
    assert post["human_approval_required"] is True
    print("test_tiktok_mcp_tools passed")


if __name__ == "__main__":
    main()

