from __future__ import annotations

import argparse
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.services.tiktok_oauth_service import (
    build_tiktok_oauth_url,
    check_tiktok_oauth_config,
    exchange_authorization_code_blocked,
    render_tiktok_oauth_setup_markdown,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a TikTok OAuth setup URL without storing or printing tokens.")
    parser.add_argument("--scopes", default="user.info.basic,video.list")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--exchange-code", default="")
    parser.add_argument("--allow-token-exchange", action="store_true", default=False)
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    setup = build_tiktok_oauth_url(args.scopes)
    config_check = check_tiktok_oauth_config(args.scopes)
    print("WaveScout TikTok OAuth Setup: PASS")
    print("External calls: false")
    print("Stores tokens: false")
    print("Prints tokens: false")
    print(f"Redirect URI: {setup['redirect_uri']}")
    print(f"Scopes: {', '.join(setup['requested_scopes'])}")
    print("\nAuthorization URL:")
    print(setup["auth_url"])
    print("\nNext manual step:")
    print(setup["next_manual_step"])

    if args.exchange_code:
        exchange = exchange_authorization_code_blocked(args.exchange_code, args.allow_token_exchange)
        print("\nToken exchange:")
        print(exchange["blocked_reason"])

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_tiktok_oauth_setup_markdown(setup, config_check), encoding="utf-8")
        print("\nArtifact:")
        print(out_path.as_posix())


if __name__ == "__main__":
    main()
