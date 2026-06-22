from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import AppConfig
from app.services.tiktok_oauth_service import (
    build_tiktok_oauth_url,
    check_tiktok_oauth_config,
    exchange_authorization_code_blocked,
)


def main() -> None:
    config = AppConfig(
        tiktok_client_key="client_key_public",
        tiktok_redirect_uri="https://example.com/callback",
        tiktok_scopes="user.info.basic,video.list",
        tiktok_access_token="secret_access_token",
    )
    setup = build_tiktok_oauth_url("user.info.basic,video.list", config)
    assert setup["external_calls"] is False
    assert setup["stores_tokens"] is False
    assert "secret_access_token" not in str(setup)
    assert "user.info.basic" in setup["auth_url"]
    check = check_tiktok_oauth_config("user.info.basic,video.list", config)
    assert check["configured"] is True
    assert "secret_access_token" not in str(check)
    exchange = exchange_authorization_code_blocked("CODE", allow_token_exchange=True, config=config)
    assert exchange["blocked"] is True
    assert exchange["external_calls"] is False
    print("test_tiktok_oauth_service passed")


if __name__ == "__main__":
    main()
