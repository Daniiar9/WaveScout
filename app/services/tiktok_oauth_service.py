from __future__ import annotations

from urllib.parse import urlencode

from app.config import AppConfig, load_config
from app.services.live_discovery_gate import default_live_safety_status
from app.services.tiktok_capability_service import parse_approved_scopes

DEFAULT_TIKTOK_SCOPES = ["user.info.basic", "video.list"]
TIKTOK_AUTHORIZE_URL = "https://www.tiktok.com/v2/auth/authorize/"


def build_tiktok_oauth_url(
    requested_scopes: str | list[str] | None = None,
    config: AppConfig | None = None,
    state: str = "wavescout_manual_setup",
) -> dict:
    config = config or load_config()
    scopes = _coerce_scopes(requested_scopes)
    client_key = config.tiktok_client_key or "SET_TIKTOK_CLIENT_KEY"
    redirect_uri = config.tiktok_redirect_uri or "SET_TIKTOK_REDIRECT_URI"
    query = urlencode(
        {
            "client_key": client_key,
            "response_type": "code",
            "scope": ",".join(scopes),
            "redirect_uri": redirect_uri,
            "state": state,
        }
    )
    return {
        "auth_url": f"{TIKTOK_AUTHORIZE_URL}?{query}",
        "redirect_uri": redirect_uri,
        "requested_scopes": scopes,
        "external_calls": False,
        "stores_tokens": False,
        "prints_tokens": False,
        "safety_status": default_live_safety_status(dry_run=True, external_calls=False),
        "next_manual_step": "Open the URL yourself, approve scopes in TikTok, then store returned credentials only in local environment variables.",
    }


def check_tiktok_oauth_config(
    requested_scopes: str | list[str] | None = None,
    config: AppConfig | None = None,
) -> dict:
    config = config or load_config()
    requested = _coerce_scopes(requested_scopes)
    configured_scopes = _configured_scopes(config)
    missing = []
    if not config.tiktok_client_key:
        missing.append("TIKTOK_CLIENT_KEY")
    if not config.tiktok_redirect_uri:
        missing.append("TIKTOK_REDIRECT_URI")
    missing_scopes = [scope for scope in requested if scope not in configured_scopes]
    return {
        "configured": not missing and not missing_scopes,
        "missing_config": missing,
        "requested_scopes": requested,
        "configured_scopes": configured_scopes,
        "missing_scopes": missing_scopes,
        "has_client_secret": bool(config.tiktok_client_secret),
        "has_access_token": bool(config.tiktok_access_token),
        "has_refresh_token": bool(config.tiktok_refresh_token),
        "prints_tokens": False,
        "stores_tokens": False,
        "external_calls": False,
        "safety_status": default_live_safety_status(dry_run=True, external_calls=False),
    }


def exchange_authorization_code_blocked(
    code: str,
    allow_token_exchange: bool = False,
    config: AppConfig | None = None,
) -> dict:
    config = config or load_config()
    reason = "Token exchange is not implemented in this pass; no tokens were requested, printed, or stored."
    if allow_token_exchange:
        reason = "Token exchange requested, but live token exchange requires a separate audited HTTP implementation."
    return {
        "exchange_requested": bool(code),
        "allow_token_exchange": allow_token_exchange,
        "blocked": True,
        "blocked_reason": reason,
        "external_calls": False,
        "stores_tokens": False,
        "prints_tokens": False,
        "has_client_key": bool(config.tiktok_client_key),
        "has_client_secret": bool(config.tiktok_client_secret),
        "safety_status": default_live_safety_status(dry_run=True, external_calls=False),
    }


def render_tiktok_oauth_setup_markdown(setup: dict, config_check: dict | None = None) -> str:
    check = config_check or {}
    return f"""# TikTok OAuth Setup

- External calls: false
- Stores tokens: false
- Prints tokens: false
- Redirect URI: {setup.get("redirect_uri", "")}
- Requested scopes: {", ".join(setup.get("requested_scopes", []))}

## Authorization URL

{setup.get("auth_url", "")}

## Config Check

- Configured: {str(check.get("configured", False)).lower()}
- Missing config: {", ".join(check.get("missing_config", [])) or "None"}
- Missing scopes: {", ".join(check.get("missing_scopes", [])) or "None"}

## Next Manual Step

{setup.get("next_manual_step", "")}
"""


def _coerce_scopes(requested_scopes: str | list[str] | None) -> list[str]:
    if requested_scopes is None:
        return list(DEFAULT_TIKTOK_SCOPES)
    if isinstance(requested_scopes, str):
        return parse_approved_scopes(requested_scopes)
    return parse_approved_scopes(",".join(requested_scopes))


def _configured_scopes(config: AppConfig) -> list[str]:
    return parse_approved_scopes(",".join([config.tiktok_scopes, config.tiktok_approved_scopes]))
