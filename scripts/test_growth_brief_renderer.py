from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.services.growth_brief_renderer import render_growth_brief_markdown
from app.services.growth_engine import run_growth_engine


def main() -> None:
    growth_brief = run_growth_engine(product_text="An AI workspace that connects your apps into workflows.")
    markdown = render_growth_brief_markdown(growth_brief)
    assert "# WaveScout Growth Brief" in markdown
    assert "## Safety Status" in markdown
    assert "external_calls=false" in markdown
    assert "tiktok_dm_send=false" in markdown
    assert "send_allowed=false" in markdown
    print("test_growth_brief_renderer passed")


if __name__ == "__main__":
    main()

