from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import AppConfig
from app.services.tiktok_research_discovery import check_tiktok_research_live


def main() -> None:
    status = check_tiktok_research_live(
        query="AI workflow automation",
        config=AppConfig(),
        allow_tiktok_live=True,
        dry_run=False,
    )
    assert status["blocked"] is True
    assert status["external_calls"] is False
    assert status["tiktok_live_calls"] is False
    assert status["raw_results"] == []
    assert status["safety_status"]["tiktok_scraping"] is False
    print("test_tiktok_research_live passed")


if __name__ == "__main__":
    main()
