from __future__ import annotations

import json
from dataclasses import dataclass

from app.config import AppConfig, load_config
from app.models.common import to_plain_dict
from app.models.tiktok_capability import TikTokActionGate, TikTokCapability, TikTokCapabilityReport


@dataclass(frozen=True)
class CapabilitySpec:
    name: str
    description: str
    category: str
    official_api: str
    endpoint: str
    use: str
    required_scopes: list[str]
    config_flags: list[str]
    docs_url: str
    default_status: str
    external_call_required: bool = True
    live_mode_supported: bool = False


CAPABILITY_SPECS = [
    CapabilitySpec(
        name="display_user_info",
        description="Read authorized account/profile metadata.",
        category="display",
        official_api="Display API",
        endpoint="/v2/user/info/",
        use="Authorized account/profile metadata.",
        required_scopes=["user.info.basic"],
        config_flags=["TIKTOK_OFFICIAL_API_ENABLED", "TIKTOK_DISPLAY_API_ENABLED"],
        docs_url="https://developers.tiktok.com/",
        default_status="dry_run_only",
    ),
    CapabilitySpec(
        name="display_list_videos",
        description="List authorized user's recent/public videos.",
        category="display",
        official_api="Display API",
        endpoint="/v2/video/list/",
        use="Authorized user recent/public videos.",
        required_scopes=["video.list"],
        config_flags=["TIKTOK_OFFICIAL_API_ENABLED", "TIKTOK_DISPLAY_API_ENABLED"],
        docs_url="https://developers.tiktok.com/",
        default_status="dry_run_only",
    ),
    CapabilitySpec(
        name="display_query_videos",
        description="Query selected authorized-user videos.",
        category="display",
        official_api="Display API",
        endpoint="/v2/video/query/",
        use="Authorized user selected videos.",
        required_scopes=["video.list"],
        config_flags=["TIKTOK_OFFICIAL_API_ENABLED", "TIKTOK_DISPLAY_API_ENABLED"],
        docs_url="https://developers.tiktok.com/",
        default_status="dry_run_only",
    ),
    CapabilitySpec(
        name="research_query_videos",
        description="Query approved public video metadata by research filters.",
        category="research",
        official_api="Research API",
        endpoint="/v2/research/video/query/",
        use="Future trend/creator discovery where approved.",
        required_scopes=["research.data.basic"],
        config_flags=["TIKTOK_OFFICIAL_API_ENABLED", "TIKTOK_RESEARCH_API_ENABLED"],
        docs_url="https://developers.tiktok.com/",
        default_status="blocked",
    ),
    CapabilitySpec(
        name="research_query_comments",
        description="Query approved public comments metadata.",
        category="research",
        official_api="Research API",
        endpoint="official research comments endpoint placeholder",
        use="Future comment intelligence where approved.",
        required_scopes=["research.data.basic"],
        config_flags=["TIKTOK_OFFICIAL_API_ENABLED", "TIKTOK_RESEARCH_API_ENABLED"],
        docs_url="https://developers.tiktok.com/",
        default_status="blocked",
    ),
    CapabilitySpec(
        name="content_direct_post",
        description="Post to an authorized user account.",
        category="content_posting",
        official_api="Content Posting API",
        endpoint="official content direct-post endpoint placeholder",
        use="Authorized posting only; not part of creator scouting.",
        required_scopes=["video.publish"],
        config_flags=["TIKTOK_OFFICIAL_API_ENABLED", "TIKTOK_CONTENT_POSTING_API_ENABLED"],
        docs_url="https://developers.tiktok.com/",
        default_status="blocked",
    ),
    CapabilitySpec(
        name="tiktok_dm_send",
        description="TikTok DM sending is not supported by WaveScout.",
        category="blocked",
        official_api="none implemented",
        endpoint="",
        use="Not supported.",
        required_scopes=[],
        config_flags=[],
        docs_url="",
        default_status="blocked",
        external_call_required=False,
        live_mode_supported=False,
    ),
]


def parse_approved_scopes(scope_string: str) -> list[str]:
    raw = scope_string.replace(",", " ").replace(";", " ").split()
    seen: set[str] = set()
    scopes: list[str] = []
    for scope in raw:
        cleaned = scope.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            scopes.append(cleaned)
    return scopes


def build_tiktok_capability_report(config: AppConfig | None = None) -> TikTokCapabilityReport:
    config = config or load_config()
    approved_scopes = parse_approved_scopes(config.tiktok_approved_scopes)
    capabilities = [_build_capability(spec, config, approved_scopes) for spec in CAPABILITY_SPECS]
    return TikTokCapabilityReport(
        capabilities=capabilities,
        approved_scopes=approved_scopes,
        available=[capability.name for capability in capabilities if capability.status == "available"],
        dry_run_only=[capability.name for capability in capabilities if capability.status == "dry_run_only"],
        blocked=[capability.name for capability in capabilities if capability.status == "blocked"],
        not_configured=[capability.name for capability in capabilities if capability.status == "not_configured"],
        external_calls_made=False,
        scraping_enabled=False,
        dm_send_enabled=False,
        live_post_allowed=False,
        human_approval_required=True,
        summary="TikTok connector readiness checked without network calls.",
    )


def check_capability(name: str, config: AppConfig | None = None) -> TikTokCapability:
    report = build_tiktok_capability_report(config)
    for capability in report.capabilities:
        if capability.name == name:
            return capability
    raise ValueError(f"Unknown TikTok capability: {name}")


def require_capability(name: str, config: AppConfig | None = None) -> TikTokActionGate:
    capability = check_capability(name, config)
    if capability.action_gate is None:
        raise ValueError(f"Capability has no action gate: {name}")
    return capability.action_gate


def render_capability_report_markdown(report: TikTokCapabilityReport) -> str:
    return f"""# TikTok Capability Report

## Summary

{report.summary}

- External calls made: {str(report.external_calls_made).lower()}
- TikTok scraping enabled: {str(report.scraping_enabled).lower()}
- TikTok DM/send enabled: {str(report.dm_send_enabled).lower()}
- Live post allowed: {str(report.live_post_allowed).lower()}
- Human approval required: {str(report.human_approval_required).lower()}
- Approved scopes: {", ".join(report.approved_scopes) if report.approved_scopes else "None configured"}

## Capability Matrix

| Capability | Official API | Required Scopes | Status | Missing Scopes | Missing Config | External Call Required | Human Approval Required | Reason |
|---|---|---|---|---|---|---|---|---|
{_capability_rows(report.capabilities)}

## Dry-Run Available

{_bullets(report.dry_run_only)}

## Blocked

{_bullets(report.blocked)}

## Safety Status

- external_calls=false
- scraping=false
- tiktok_dm=false
- live_post_allowed=false
- human_approval_required=true
"""


def render_capability_report_json(report: TikTokCapabilityReport) -> str:
    return json.dumps(to_plain_dict(report), indent=2, sort_keys=True)


def build_oauth_setup_instructions(scopes: list[str] | None = None) -> dict:
    requested_scopes = scopes or ["user.info.basic", "video.list"]
    return {
        "external_calls": False,
        "opens_browser": False,
        "stores_tokens": False,
        "requested_scopes": requested_scopes,
        "checklist": [
            "Create a TikTok developer app.",
            "Configure the redirect URI in the developer app and local environment.",
            "Request only the scopes needed for the capability being tested.",
            "Run the capability checker before attempting live work.",
            "Use dry-run adapters until a separate live-mode review is approved.",
            "Store credentials only in local environment variables.",
            "Do not automate DMs or message sending.",
        ],
    }


def _build_capability(
    spec: CapabilitySpec,
    config: AppConfig,
    approved_scopes: list[str],
) -> TikTokCapability:
    missing_scopes = [scope for scope in spec.required_scopes if scope not in approved_scopes]
    missing_flags = _missing_flags(spec, config)
    has_credentials = bool(config.tiktok_client_key and config.tiktok_access_token)
    missing_credentials = [] if has_credentials or spec.name == "tiktok_dm_send" else ["TIKTOK_CLIENT_KEY", "TIKTOK_ACCESS_TOKEN"]
    if spec.name == "tiktok_dm_send":
        status = "blocked"
        reason = "WaveScout does not automate TikTok DMs."
        live_confirm = False
    elif spec.category == "display":
        status = "dry_run_only"
        reason = _dry_run_reason("Display API", missing_flags, missing_scopes, missing_credentials)
        live_confirm = config.tiktok_live_display_confirm
    elif spec.category == "research":
        live_confirm = config.tiktok_live_research_confirm
        if missing_flags or missing_scopes:
            status = "blocked"
            reason = "Research API blocked until research flag is enabled and research.data.basic is approved."
        else:
            status = "dry_run_only"
            reason = _dry_run_reason("Research API", missing_flags, missing_scopes, missing_credentials)
    elif spec.category == "content_posting":
        live_confirm = config.tiktok_live_post_confirm
        status = "blocked"
        reason = (
            "Content posting requires video.publish, user authorization, explicit live confirmation, "
            "human approval, and a separate live implementation audit."
        )
    else:
        status = spec.default_status
        reason = "Capability is not implemented."
        live_confirm = False

    missing_config = missing_flags + missing_credentials
    gate = TikTokActionGate(
        capability_name=spec.name,
        allowed=False,
        reason=_gate_reason(status, reason, config, missing_scopes, missing_config, live_confirm),
        required_scopes=spec.required_scopes,
        missing_scopes=missing_scopes,
        external_call_required=spec.external_call_required,
        live_mode_required=spec.external_call_required,
        human_approval_required=True,
    )
    return TikTokCapability(
        name=spec.name,
        description=spec.description,
        category=spec.category,
        official_api=spec.official_api,
        endpoint=spec.endpoint,
        use=spec.use,
        required_scopes=spec.required_scopes,
        config_flags=spec.config_flags,
        external_call_required=spec.external_call_required,
        live_mode_supported=spec.live_mode_supported,
        status=status,
        reason=reason,
        docs_url=spec.docs_url,
        missing_scopes=missing_scopes,
        missing_config_flags=missing_config,
        action_gate=gate,
    )


def _missing_flags(spec: CapabilitySpec, config: AppConfig) -> list[str]:
    flag_values = {
        "TIKTOK_OFFICIAL_API_ENABLED": config.tiktok_official_api_enabled,
        "TIKTOK_DISPLAY_API_ENABLED": config.tiktok_display_api_enabled,
        "TIKTOK_RESEARCH_API_ENABLED": config.tiktok_research_api_enabled,
        "TIKTOK_CONTENT_POSTING_API_ENABLED": config.tiktok_content_posting_api_enabled,
    }
    return [flag for flag in spec.config_flags if not flag_values.get(flag, False)]


def _dry_run_reason(api_name: str, missing_flags: list[str], missing_scopes: list[str], missing_credentials: list[str]) -> str:
    blockers = missing_flags + missing_scopes + missing_credentials
    if blockers:
        return f"{api_name} dry-run available; live mode is not configured. Missing: {', '.join(blockers)}."
    return f"{api_name} dry-run available; live HTTP is intentionally not implemented in this readiness pass."


def _gate_reason(
    status: str,
    reason: str,
    config: AppConfig,
    missing_scopes: list[str],
    missing_config: list[str],
    live_confirm: bool,
) -> str:
    if config.wavescout_offline_mode:
        return f"Blocked for live use because WAVESCOUT_OFFLINE_MODE=true. {reason}"
    if not config.wavescout_allow_external_calls:
        return f"Blocked for live use because WAVESCOUT_ALLOW_EXTERNAL_CALLS=false. {reason}"
    if missing_config:
        return f"Blocked for live use; missing config: {', '.join(missing_config)}. {reason}"
    if missing_scopes:
        return f"Blocked for live use; missing scopes: {', '.join(missing_scopes)}. {reason}"
    if not live_confirm:
        return f"Blocked for live use; explicit live confirmation flag is false. {reason}"
    return f"Blocked for live use; live HTTP not implemented in this pass. {reason}"


def _capability_rows(capabilities: list[TikTokCapability]) -> str:
    rows = []
    for capability in capabilities:
        rows.append(
            "| "
            + " | ".join(
                [
                    _cell(capability.name),
                    _cell(capability.official_api),
                    _cell(", ".join(capability.required_scopes) or "None"),
                    _cell(capability.status),
                    _cell(", ".join(capability.missing_scopes) or "None"),
                    _cell(", ".join(capability.missing_config_flags) or "None"),
                    str(capability.external_call_required).lower(),
                    str(True).lower(),
                    _cell(capability.reason),
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def _cell(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)

