from __future__ import annotations

import argparse
from urllib.parse import urlencode

from bootstrap import bootstrap

bootstrap()

from app.config import load_config
from app.services.tiktok_capability_service import build_oauth_setup_instructions, parse_approved_scopes

AUTH_URL_BASE = "https://www.tiktok.com/v2/auth/authorize/"


def build_oauth_url(scopes: list[str], redirect_uri: str | None = None, state: str | None = None) -> dict:
    config = load_config()
    missing = []
    if not config.tiktok_client_key:
        missing.append("TIKTOK_CLIENT_KEY")
    resolved_redirect_uri = redirect_uri or config.tiktok_redirect_uri
    if not resolved_redirect_uri:
        missing.append("TIKTOK_REDIRECT_URI or --redirect-uri")
    instructions = build_oauth_setup_instructions(scopes)
    if missing:
        return {
            "dry_run": True,
            "external_calls_made": False,
            "opens_browser": False,
            "exchanges_tokens": False,
            "stores_tokens": False,
            "missing": missing,
            "authorization_url_preview": "",
            "instructions": instructions,
            "note": "Add local env placeholders before constructing a URL. Do not commit secrets.",
        }
    query = {
        "client_key": config.tiktok_client_key,
        "scope": ",".join(scopes),
        "response_type": "code",
        "redirect_uri": resolved_redirect_uri,
    }
    if state:
        query["state"] = state
    return {
        "dry_run": True,
        "external_calls_made": False,
        "opens_browser": False,
        "exchanges_tokens": False,
        "stores_tokens": False,
        "missing": [],
        "authorization_url_preview": f"{AUTH_URL_BASE}?{urlencode(query)}",
        "instructions": instructions,
        "note": "Verify exact TikTok OAuth parameters in official docs before enabling live OAuth.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a TikTok OAuth setup URL preview without opening a browser.")
    parser.add_argument("--scopes", default="user.info.basic,video.list")
    parser.add_argument("--redirect-uri", default="")
    parser.add_argument("--state", default="")
    parser.add_argument("--dry-run", action="store_true", default=True)
    args = parser.parse_args()
    scopes = parse_approved_scopes(args.scopes)
    result = build_oauth_url(scopes, args.redirect_uri or None, args.state or None)
    print("TikTok OAuth URL Builder: DRY RUN")
    print("External calls: false")
    print("Browser opened: false")
    print("Tokens exchanged: false")
    if result["missing"]:
        print("Missing:")
        for item in result["missing"]:
            print(f"- {item}")
    if result["authorization_url_preview"]:
        print("Authorization URL preview:")
        print(result["authorization_url_preview"])
    print(result["note"])


if __name__ == "__main__":
    main()

