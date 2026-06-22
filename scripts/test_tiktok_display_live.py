from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import AppConfig
from app.services.tiktok_owned_account_live import check_tiktok_owned_account_live


def main() -> None:
    status = check_tiktok_owned_account_live(
        AppConfig(),
        allow_tiktok_live=True,
        dry_run=False,
        handle="@demoapp",
    )
    assert status["blocked"] is True
    assert status["external_calls"] is False
    assert status["tiktok_live_calls"] is False
    assert status["safety_status"]["send_allowed"] is False
    assert "WAVESCOUT_ALLOW_TIKTOK_LIVE=false" in status["blocked_reason"]
    print("test_tiktok_display_live passed")


if __name__ == "__main__":
    main()
