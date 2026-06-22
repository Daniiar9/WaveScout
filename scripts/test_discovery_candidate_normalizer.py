from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.services.discovery_candidate_normalizer import normalize_discovery_candidate
from app.services.discovery_dedupe import dedupe_discovery_candidates, rank_discovery_candidates_initial
from app.services.scout_planner import build_scout_run_plan


def main() -> None:
    raw = {"handle": "agentbuilder", "source": "manual_import", "confidence": 0.7, "raw_snippet": "AI workflow demos"}
    candidate = normalize_discovery_candidate(raw)
    duplicate = normalize_discovery_candidate({"handle": "@agentbuilder", "source": "search"})
    assert candidate.handle == "@agentbuilder"
    assert candidate.platform == "tiktok"
    deduped = dedupe_discovery_candidates([candidate, duplicate])
    assert len(deduped) == 1
    plan = build_scout_run_plan(product_text="An AI workspace for workflow automation.")
    ranked = rank_discovery_candidates_initial(deduped, plan.search_strategy)
    assert ranked[0].handle == "@agentbuilder"
    print("test_discovery_candidate_normalizer passed")


if __name__ == "__main__":
    main()

