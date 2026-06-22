from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.services.product_intelligence import build_product_intelligence_from_text
from app.services.trend_wave_mapper import build_trend_wave_map, render_trend_wave_map_markdown

PRODUCT_TEXT = "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows."


def main() -> None:
    brief = build_product_intelligence_from_text(PRODUCT_TEXT)
    wave_map = build_trend_wave_map(brief)
    assert "talk to your apps" in wave_map.primary_waves
    assert "AI workspace" in wave_map.primary_waves
    assert "generic ChatGPT tips" in wave_map.rejected_waves
    assert "AI workflow demo creators" in wave_map.creator_archetypes
    assert "#AIWorkspace" in wave_map.hashtags
    assert "Trend Wave Map" in render_trend_wave_map_markdown(wave_map)
    print("test_trend_wave_mapper passed")


if __name__ == "__main__":
    main()

