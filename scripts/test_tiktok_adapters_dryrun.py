from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import AppConfig
from app.adapters.tiktok_content_posting_api import direct_post_video_dry_run, query_creator_info_dry_run
from app.adapters.tiktok_display_api import get_user_info_dry_run, list_videos_dry_run, query_videos_dry_run
from app.adapters.tiktok_research_api import query_comments_dry_run, query_videos_dry_run as research_query_videos_dry_run


def main() -> None:
    config = AppConfig()
    responses = [
        get_user_info_dry_run(config),
        list_videos_dry_run(config),
        query_videos_dry_run(["video_1"], config),
        research_query_videos_dry_run({"hashtag": "AIWorkspace"}, ["id"], config),
        query_comments_dry_run("video_1", config),
        query_creator_info_dry_run(config),
        direct_post_video_dry_run({"title": "draft"}, config),
    ]
    for response in responses:
        assert response["dry_run"] is True
        assert response["external_calls_made"] is False
        assert response["human_approval_required"] is True
        assert response["gate"]["allowed"] is False
    post = responses[-1]
    assert post["live_post_allowed"] is False
    assert post["send_allowed"] is False
    print("test_tiktok_adapters_dryrun passed")


if __name__ == "__main__":
    main()

