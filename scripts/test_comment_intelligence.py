from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.services.comment_intelligence import (
    calculate_comment_intent_quality,
    classify_comment,
    extract_comment_signals,
    summarize_comment_intelligence,
)


def main() -> None:
    high_comments = [
        "Can this connect to Notion?",
        "Does it work with Slack?",
        "I need this for my CRM.",
        "Can you make a tutorial?",
    ]
    low_comments = ["first", "AI is crazy", "bro what", "follow me"]
    assert classify_comment("Can this connect to Notion?")["intent_type"] == "asks_for_tool"
    assert classify_comment("AI is crazy")["intent_type"] == "generic_hype"
    signals = extract_comment_signals(high_comments, "creator_test")
    summary = summarize_comment_intelligence(signals)
    assert summary["quality"] == "high"
    assert "Notion" in summary["tool_mentions"]
    assert "Slack" in summary["tool_mentions"]
    assert calculate_comment_intent_quality(signals) >= 15
    low_summary = summarize_comment_intelligence(extract_comment_signals(low_comments, "creator_test"))
    assert low_summary["quality"] == "low"
    print("test_comment_intelligence passed")


if __name__ == "__main__":
    main()

