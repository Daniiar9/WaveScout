from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.services.product_intelligence import (
    build_product_intelligence_from_text,
    build_product_intelligence_from_url,
    render_product_brief_markdown,
)


PRODUCT_TEXT = "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows."


def main() -> None:
    brief = build_product_intelligence_from_text(PRODUCT_TEXT, "https://example.com")
    assert brief.product_url == "https://example.com"
    assert brief.category == "AI workspace / connected SaaS stack"
    assert "AI workspace" in brief.trend_keywords
    assert brief.creator_relevant_angles
    assert "Product Intelligence Brief" in render_product_brief_markdown(brief)
    url_brief = build_product_intelligence_from_url("https://example.com", allow_fetch=False)
    assert url_brief.confidence < 0.5
    assert "URL fetch was not performed" in " ".join(url_brief.evidence)
    print("test_product_intelligence passed")


if __name__ == "__main__":
    main()

