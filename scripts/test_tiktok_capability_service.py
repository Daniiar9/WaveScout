from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import AppConfig
from app.services.tiktok_capability_service import (
    build_tiktok_capability_report,
    check_capability,
    parse_approved_scopes,
    render_capability_report_json,
    render_capability_report_markdown,
)


def main() -> None:
    config = AppConfig()
    report = build_tiktok_capability_report(config)
    by_name = {capability.name: capability for capability in report.capabilities}
    assert report.external_calls_made is False
    assert report.scraping_enabled is False
    assert report.dm_send_enabled is False
    assert report.live_post_allowed is False
    assert by_name["display_user_info"].status in {"dry_run_only", "not_configured"}
    assert by_name["display_list_videos"].status in {"dry_run_only", "not_configured"}
    assert by_name["research_query_videos"].status == "blocked"
    assert "research.data.basic" in by_name["research_query_videos"].missing_scopes
    assert by_name["content_direct_post"].status == "blocked"
    assert by_name["tiktok_dm_send"].status == "blocked"
    assert by_name["tiktok_dm_send"].action_gate.allowed is False
    assert parse_approved_scopes("user.info.basic, video.list;video.list") == ["user.info.basic", "video.list"]
    assert check_capability("content_direct_post", config).action_gate.allowed is False
    assert "TikTok Capability Report" in render_capability_report_markdown(report)
    assert '"external_calls_made": false' in render_capability_report_json(report)
    print("test_tiktok_capability_service passed")


if __name__ == "__main__":
    main()

