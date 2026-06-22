from __future__ import annotations

import json
import re
from typing import Any

from app.config import AppConfig, load_config
from app.models import CreatorSearchStrategy, DiscoveryCandidateNormalized, LiveDiscoveryRequest, LiveDiscoveryResponse
from app.services.discovery_candidate_normalizer import normalize_discovery_candidate
from app.services.text import normalize_handle, unique_keep_order

PROVIDER_CONFIG = {
    "exa": {
        "display_name": "Exa",
        "api_key_attr": "exa_api_key",
        "required_env": "EXA_API_KEY",
        "endpoint": "https://api.exa.ai/search",
        "schema_status": "provider integration pending exact API schema.",
    },
    "serp": {
        "display_name": "SERP",
        "api_key_attr": "serp_api_key",
        "required_env": "SERP_API_KEY",
        "endpoint": "provider-specific search endpoint",
        "schema_status": "provider integration pending exact API schema.",
    },
}


def default_live_safety_status(
    *,
    dry_run: bool = True,
    external_calls: bool = False,
    tiktok_live_calls: bool = False,
) -> dict:
    return {
        "dry_run": dry_run,
        "external_calls": external_calls,
        "tiktok_live_calls": tiktok_live_calls,
        "tiktok_scraping": False,
        "browser_automation": False,
        "tiktok_dm_send": False,
        "message_sending": False,
        "live_post": False,
        "send_allowed": False,
        "approval_required": True,
        "human_review_required": True,
    }


def build_live_discovery_request(
    strategy: CreatorSearchStrategy | dict,
    provider: str = "dry_run_search",
    limit: int = 25,
    allow_external: bool = False,
    dry_run: bool = True,
) -> LiveDiscoveryRequest:
    data = strategy if isinstance(strategy, dict) else strategy.__dict__
    queries = unique_keep_order(list(data.get("search_queries", []) or []), 10)
    hashtags = unique_keep_order(list(data.get("hashtags", []) or []), 12)
    product_context = str(data.get("product_context", "") or data.get("product_id", "") or "")
    return LiveDiscoveryRequest(
        provider=provider,
        queries=queries,
        hashtags=hashtags,
        limit=max(1, min(int(limit), 50)),
        allow_external=allow_external,
        dry_run=dry_run,
        product_context=product_context,
        safety_status=default_live_safety_status(dry_run=dry_run, external_calls=False),
    )


def check_live_discovery_provider(
    provider: str,
    config: AppConfig | None = None,
    allow_external: bool = False,
) -> dict:
    config = config or load_config()
    normalized_provider = _provider_name(provider)
    if normalized_provider in {"dry_run_search", "manual"}:
        return {
            "provider": normalized_provider,
            "allowed": False,
            "status": "dry_run_only",
            "blocked_reason": "Provider runs without live external calls.",
            "required_env_vars": [],
            "missing_env_vars": [],
            "capability_check_passed": True,
            "external_calls": False,
            "safety_status": default_live_safety_status(dry_run=True, external_calls=False),
        }
    provider_config = PROVIDER_CONFIG.get(normalized_provider)
    if not provider_config:
        return {
            "provider": normalized_provider,
            "allowed": False,
            "status": "blocked",
            "blocked_reason": f"Unknown live discovery provider: {provider}.",
            "required_env_vars": [],
            "missing_env_vars": [],
            "capability_check_passed": False,
            "external_calls": False,
            "safety_status": default_live_safety_status(dry_run=True, external_calls=False),
        }
    required_env = provider_config["required_env"]
    has_api_key = bool(getattr(config, provider_config["api_key_attr"]))
    missing_env = [] if has_api_key else [required_env]
    if not allow_external:
        reason = "Blocked because explicit CLI/tool allow_external flag was not provided."
        status = "dry_run_only"
    elif not config.wavescout_allow_external_calls:
        reason = "Blocked because WAVESCOUT_ALLOW_EXTERNAL_CALLS=false."
        status = "blocked"
    elif missing_env:
        reason = f"Blocked because missing provider credential: {required_env}."
        status = "blocked"
    else:
        reason = provider_config["schema_status"]
        status = "blocked"
    return {
        "provider": normalized_provider,
        "allowed": False,
        "status": status,
        "blocked_reason": reason,
        "required_env_vars": [required_env],
        "missing_env_vars": missing_env,
        "capability_check_passed": allow_external and config.wavescout_allow_external_calls and not missing_env,
        "external_calls": False,
        "safety_status": default_live_safety_status(dry_run=True, external_calls=False),
    }


def run_live_discovery_request(
    request: LiveDiscoveryRequest,
    config: AppConfig | None = None,
) -> LiveDiscoveryResponse:
    provider = _provider_name(request.provider)
    if provider == "exa":
        return run_exa_discovery(request, config)
    if provider == "serp":
        return run_serp_discovery(request, config)
    if provider in {"dry_run_search", "manual"}:
        return _dry_run_response(
            provider=provider,
            request=request,
            blocked_reason="Provider is dry-run/manual by design; no external calls were attempted.",
        )
    return LiveDiscoveryResponse(
        provider=provider,
        dry_run=True,
        external_calls=False,
        blocked_reason=f"Unknown live discovery provider: {request.provider}.",
        payloads=[],
        raw_results=[],
        normalized_candidates=[],
        safety_status=default_live_safety_status(dry_run=True, external_calls=False),
    )


def run_exa_discovery(request: LiveDiscoveryRequest, config: AppConfig | None = None) -> LiveDiscoveryResponse:
    return _run_search_provider("exa", request, config)


def run_serp_discovery(request: LiveDiscoveryRequest, config: AppConfig | None = None) -> LiveDiscoveryResponse:
    return _run_search_provider("serp", request, config)


def normalize_search_result_to_candidate(result: dict) -> DiscoveryCandidateNormalized:
    profile_url = str(result.get("profile_url") or result.get("url") or "")
    title = str(result.get("title") or "")
    snippet = str(result.get("snippet") or result.get("text") or result.get("description") or "")
    handle = str(result.get("handle") or _handle_from_url(profile_url) or _handle_from_text(title + " " + snippet))
    confidence = _source_confidence(result)
    return normalize_discovery_candidate(
        {
            "handle": handle,
            "display_name": result.get("display_name") or title,
            "profile_url": profile_url,
            "platform": "tiktok",
            "bio": snippet,
            "matched_query": result.get("matched_query", ""),
            "matched_wave": result.get("matched_wave", ""),
            "matched_hashtags": result.get("matched_hashtags", []),
            "source_provider": result.get("source_provider", "live_discovery"),
            "source_confidence": confidence,
            "reason_found": result.get("reason_found", "Search result matched WaveScout creator discovery query."),
            "raw_snippet": snippet,
            "requires_manual_review": True,
        }
    )


def render_live_discovery_markdown(response: LiveDiscoveryResponse) -> str:
    candidates = [
        f"- {candidate.handle} ({candidate.source_provider}) confidence={candidate.source_confidence}"
        for candidate in response.normalized_candidates
    ]
    return f"""# Live Discovery Gate: {response.provider}

- Dry run: {str(response.dry_run).lower()}
- External calls: {str(response.external_calls).lower()}
- Blocked reason: {response.blocked_reason or "None"}

## Payloads
```json
{json.dumps(response.payloads, indent=2, sort_keys=True)}
```

## Normalized Candidates
{_bullets(candidates)}

## Safety Status
{_status_lines(response.safety_status)}
"""


def _run_search_provider(
    provider: str,
    request: LiveDiscoveryRequest,
    config: AppConfig | None,
) -> LiveDiscoveryResponse:
    config = config or load_config()
    provider_config = PROVIDER_CONFIG[provider]
    payloads = _build_provider_payloads(provider, request)
    if request.dry_run or not request.allow_external:
        return LiveDiscoveryResponse(
            provider=provider,
            dry_run=True,
            external_calls=False,
            blocked_reason="Dry-run payload generated; explicit external discovery was not enabled.",
            payloads=payloads,
            raw_results=[],
            normalized_candidates=[],
            safety_status=default_live_safety_status(dry_run=True, external_calls=False),
        )
    check = check_live_discovery_provider(provider, config, allow_external=request.allow_external)
    return LiveDiscoveryResponse(
        provider=provider,
        dry_run=True,
        external_calls=False,
        blocked_reason=check["blocked_reason"] or provider_config["schema_status"],
        payloads=payloads,
        raw_results=[],
        normalized_candidates=[],
        safety_status=check["safety_status"],
    )


def _dry_run_response(provider: str, request: LiveDiscoveryRequest, blocked_reason: str) -> LiveDiscoveryResponse:
    return LiveDiscoveryResponse(
        provider=provider,
        dry_run=True,
        external_calls=False,
        blocked_reason=blocked_reason,
        payloads=_build_provider_payloads(provider, request),
        raw_results=[],
        normalized_candidates=[],
        safety_status=default_live_safety_status(dry_run=True, external_calls=False),
    )


def _build_provider_payloads(provider: str, request: LiveDiscoveryRequest) -> list[dict]:
    queries = request.queries[:10] or ["TikTok creators AI workflow automation"]
    return [
        {
            "provider": provider,
            "query": query,
            "hashtags": request.hashtags[:8],
            "limit": min(request.limit, 10),
            "filters": {
                "allowed_domains": ["tiktok.com"],
                "result_type": "public_profile_or_video_url",
                "no_scraping": True,
                "no_browser_automation": True,
            },
            "external_calls": False,
        }
        for query in queries
    ]


def _provider_name(provider: str) -> str:
    return provider.strip().lower().replace("_placeholder", "")


def _handle_from_url(url: str) -> str:
    match = re.search(r"tiktok\.com/@([A-Za-z0-9._-]+)", url)
    return normalize_handle(match.group(1)) if match else ""


def _handle_from_text(text: str) -> str:
    match = re.search(r"@([A-Za-z0-9._-]+)", text)
    return normalize_handle(match.group(1)) if match else ""


def _source_confidence(result: dict[str, Any]) -> float:
    if result.get("source_confidence") is not None:
        return float(result["source_confidence"])
    url = str(result.get("profile_url") or result.get("url") or "")
    snippet = str(result.get("snippet") or result.get("description") or "")
    confidence = 0.35
    if "tiktok.com/@" in url:
        confidence += 0.35
    if any(token in snippet.lower() for token in ["tutorial", "demo", "workflow", "founder", "ai"]):
        confidence += 0.15
    return min(confidence, 0.85)


def _status_lines(status: dict) -> str:
    return "\n".join(f"- {key}={str(value).lower()}" for key, value in status.items())


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(values)
