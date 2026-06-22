from __future__ import annotations

from app.config import AppConfig, load_config
from app.models import CreatorSearchStrategy, DiscoveryProvider, DiscoveryRunResult
from app.services.discovery_candidate_normalizer import normalize_discovery_candidate
from app.services.text import stable_id
from app.adapters.manual_discovery import ManualDiscovery
from app.adapters.search_discovery_placeholder import SearchDiscoveryPlaceholder
from app.adapters.tiktok_research_discovery_placeholder import TikTokResearchDiscoveryPlaceholder


def list_discovery_providers(config: AppConfig | None = None) -> list[DiscoveryProvider]:
    config = config or load_config()
    return [
        DiscoveryProvider(
            id="provider_manual_import",
            name="manual_import",
            provider_type="manual_import",
            supports_live=False,
            requires_external_calls=False,
            status="available",
            reason="Uses human-provided imported creator JSON.",
            safety_notes=["No external calls.", "Requires manual review."],
        ),
        DiscoveryProvider(
            id="provider_dry_run_search",
            name="dry_run_search",
            provider_type="dry_run_search",
            supports_live=False,
            requires_external_calls=False,
            status="dry_run_only",
            reason="Generates search query payloads only.",
            safety_notes=["No external calls.", "No scraping."],
        ),
        DiscoveryProvider(
            id="provider_exa_placeholder",
            name="exa_placeholder",
            provider_type="exa_placeholder",
            supports_live=True,
            requires_external_calls=True,
            required_env_vars=["EXA_API_KEY"],
            status="blocked",
            reason="External provider placeholder. Live mode is not implemented.",
            safety_notes=["Requires explicit future approval.", "Dry-run payloads only."],
        ),
        DiscoveryProvider(
            id="provider_serp_placeholder",
            name="serp_placeholder",
            provider_type="serp_placeholder",
            supports_live=True,
            requires_external_calls=True,
            required_env_vars=["SERP_API_KEY"],
            status="blocked",
            reason="External search provider placeholder. Live mode is not implemented.",
            safety_notes=["Requires explicit future approval.", "Dry-run payloads only."],
        ),
        DiscoveryProvider(
            id="provider_tiktok_research_placeholder",
            name="tiktok_research_placeholder",
            provider_type="tiktok_research_placeholder",
            supports_live=True,
            requires_external_calls=True,
            required_env_vars=["TIKTOK_ACCESS_TOKEN"],
            required_scopes=["research.data.basic"],
            status="blocked" if not config.tiktok_research_api_enabled else "dry_run_only",
            reason="Official TikTok Research API placeholder. No live calls in this pass.",
            safety_notes=["No scraping.", "Uses capability checker.", "Dry-run payloads only."],
        ),
        DiscoveryProvider(
            id="provider_owned_account_placeholder",
            name="owned_account_placeholder",
            provider_type="owned_account_placeholder",
            supports_live=False,
            requires_external_calls=False,
            status="dry_run_only",
            reason="Uses owned account handle/content if manually supplied.",
            safety_notes=["No account scraping.", "No live TikTok fetch."],
        ),
    ]


def check_discovery_provider(provider_name: str, config: AppConfig | None = None) -> DiscoveryProvider:
    for provider in list_discovery_providers(config):
        if provider.name == provider_name or provider.provider_type == provider_name:
            return provider
    raise ValueError(f"Unknown discovery provider: {provider_name}")


def run_discovery_provider_dry_run(
    provider: DiscoveryProvider,
    strategy: CreatorSearchStrategy,
    limit: int = 25,
    scout_plan_id: str = "",
) -> DiscoveryRunResult:
    if provider.provider_type == "manual_import":
        result = ManualDiscovery().discover_candidates(strategy, limit=limit, live=False)
        candidates = result.candidates
        payload = {"status": result.status, "reason": result.reason}
    elif provider.provider_type == "tiktok_research_placeholder":
        result = TikTokResearchDiscoveryPlaceholder().discover_candidates(strategy, limit=limit, live=False)
        candidates = result.candidates
        payload = {"dry_run_payloads": result.dry_run_payloads, "status": result.status, "reason": result.reason}
    else:
        result = SearchDiscoveryPlaceholder().discover_candidates(strategy, limit=limit, live=False)
        candidates = result.candidates
        payload = {
            "provider": provider.name,
            "dry_run_payloads": result.dry_run_payloads,
            "status": "dry_run_only",
            "reason": provider.reason,
        }
    return DiscoveryRunResult(
        id=stable_id("discovery_run", scout_plan_id, provider.name, limit),
        scout_plan_id=scout_plan_id,
        provider=provider,
        query=", ".join(strategy.search_queries[:3]),
        dry_run=True,
        external_calls=False,
        candidates=candidates,
        payload=payload,
        blocked_reason="" if provider.status in {"available", "dry_run_only"} else provider.reason,
    )


def render_discovery_run_markdown(result: DiscoveryRunResult) -> str:
    candidate_lines = [
        f"- {candidate.handle} from {candidate.source}: {candidate.reason_found}"
        for candidate in result.candidates
    ]
    return f"""# Discovery Provider Result: {result.provider.name}

- Dry run: {str(result.dry_run).lower()}
- External calls: {str(result.external_calls).lower()}
- Provider status: {result.provider.status}
- Reason: {result.provider.reason}
- Blocked reason: {result.blocked_reason or "None"}

## Candidates
{_bullets(candidate_lines)}

## Payload
```json
{result.payload}
```
"""


def render_candidate_shortlist_markdown(candidates) -> str:
    if not candidates:
        return "No discovery candidates yet. Use dry-run queries or manual import to source candidates."
    lines = [
        "| Rank | Handle | Source | Matched Wave | Reason | Needs Review |",
        "|---:|---|---|---|---|---|",
    ]
    for index, candidate in enumerate(candidates, start=1):
        normalized = normalize_discovery_candidate(candidate)
        lines.append(
            f"| {index} | {normalized.handle} | {normalized.source_provider} | {normalized.matched_wave} | {normalized.reason_found} | {str(normalized.requires_manual_review).lower()} |"
        )
    return "\n".join(lines)


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(values)

