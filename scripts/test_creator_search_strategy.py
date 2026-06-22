from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.services.creator_search_strategy import build_creator_search_strategy, render_search_strategy_markdown
from app.services.product_intelligence import build_product_intelligence_from_text
from app.services.trend_wave_mapper import build_trend_wave_map

PRODUCT_TEXT = "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows."


def main() -> None:
    brief = build_product_intelligence_from_text(PRODUCT_TEXT)
    wave_map = build_trend_wave_map(brief)
    strategy = build_creator_search_strategy(brief, wave_map)
    assert strategy.search_queries
    assert "AI workflow demo creators" in strategy.creator_archetypes
    assert "comments ask implementation questions" in strategy.qualification_criteria
    assert "generic AI hype only" in strategy.rejection_criteria
    assert "Can this connect to Notion?" in strategy.comment_patterns_to_look_for
    assert "Creator Search Strategy" in render_search_strategy_markdown(strategy)
    print("test_creator_search_strategy passed")


if __name__ == "__main__":
    main()

