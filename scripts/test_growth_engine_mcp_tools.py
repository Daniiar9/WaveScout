from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.mcp.tools import (
    TOOL_REGISTRY,
    build_growth_brief,
    build_notion_pipeline_payload,
    check_discovery_provider,
    ingest_performance_feedback_manual,
    list_discovery_providers,
    normalize_discovery_candidates,
    run_discovery_provider_dry_run,
    run_growth_engine_dry_run,
    summarize_performance_feedback,
)


def main() -> None:
    expected = {
        "list_discovery_providers",
        "check_discovery_provider",
        "run_discovery_provider_dry_run",
        "normalize_discovery_candidates",
        "run_growth_engine_dry_run",
        "build_growth_brief",
        "build_notion_pipeline_payload",
        "ingest_performance_feedback_manual",
        "summarize_performance_feedback",
    }
    assert expected <= set(TOOL_REGISTRY)
    assert list_discovery_providers()["external_calls_made"] is False
    assert check_discovery_provider("manual_import")["provider"]["requires_external_calls"] is False
    discovery = run_discovery_provider_dry_run("dry_run_search", "An AI workspace for workflows.", 5)
    assert discovery["external_calls_made"] is False
    normalized = normalize_discovery_candidates([{"handle": "creator"}])
    assert normalized["normalized_candidates"][0]["handle"] == "@creator"
    growth = run_growth_engine_dry_run("An AI workspace for workflows.")
    assert growth["safety_status"]["send_allowed"] is False
    assert build_growth_brief("An AI workspace for workflows.")["external_calls_made"] is False
    assert build_notion_pipeline_payload("An AI workspace for workflows.")["notion_write"] is False
    feedback = ingest_performance_feedback_manual({"creator_handle": "@creator"})
    assert feedback["external_calls_made"] is False
    assert summarize_performance_feedback([{"creator_handle": "@creator"}])["summary"]["external_calls_made"] is False
    print("test_growth_engine_mcp_tools passed")


if __name__ == "__main__":
    main()

