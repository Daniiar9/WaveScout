from __future__ import annotations

from app.config import AppConfig, load_config
from app.services.tiktok_owned_account_live import check_tiktok_owned_account_live


def get_owned_account_live_status(
    config: AppConfig | None = None,
    allow_tiktok_live: bool = False,
    dry_run: bool = True,
) -> dict:
    return check_tiktok_owned_account_live(
        config=config or load_config(),
        allow_tiktok_live=allow_tiktok_live,
        dry_run=dry_run,
    )
