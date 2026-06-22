from __future__ import annotations

from app.config import AppConfig, load_config
from app.services.tiktok_research_discovery import check_tiktok_research_live


def get_tiktok_research_live_status(
    query: str = "AI workflow automation",
    config: AppConfig | None = None,
    allow_tiktok_live: bool = False,
    dry_run: bool = True,
) -> dict:
    return check_tiktok_research_live(
        query=query,
        config=config or load_config(),
        allow_tiktok_live=allow_tiktok_live,
        dry_run=dry_run,
    )
