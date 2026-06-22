from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.mcp import tools


def main() -> None:
    expected = {
        "build_live_discovery_request",
        "run_live_discovery_dry_run",
        "check_live_discovery_provider",
        "build_tiktok_oauth_url",
        "check_tiktok_oauth_config",
        "check_tiktok_owned_account_live",
        "check_tiktok_research_live",
        "run_growth_engine_with_provider_dry_run",
    }
    assert expected.issubset(tools.TOOL_REGISTRY)
    discovery = tools.run_live_discovery_dry_run(provider="exa")
    assert discovery["external_calls_made"] is False
    assert discovery["live_discovery_response"]["safety_status"]["send_allowed"] is False
    owned = tools.check_tiktok_owned_account_live()
    assert owned["external_calls_made"] is False
    assert owned["owned_account_status"]["safety_status"]["live_post"] is False
    growth = tools.run_growth_engine_with_provider_dry_run(discovery_provider="exa")
    assert growth["safety_status"]["send_allowed"] is False
    assert growth["growth_brief"]["safety_status"]["live_post"] is False
    print("test_live_integration_mcp_tools passed")


if __name__ == "__main__":
    main()
