from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import AppConfig
from app.adapters.tiktok_content_posting_api import POSTING_BLOCKED_REASON, direct_post_video_dry_run


def main() -> None:
    response = direct_post_video_dry_run({"title": "draft"}, AppConfig())
    assert response["live_post"] is False
    assert response["live_post_allowed"] is False
    assert response["content_posting_supported"] is False
    assert response["send_allowed"] is False
    assert response["blocked_reason"] == POSTING_BLOCKED_REASON
    print("test_content_posting_blocked passed")


if __name__ == "__main__":
    main()
