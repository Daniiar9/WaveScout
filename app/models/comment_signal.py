from __future__ import annotations

from dataclasses import dataclass, field


INTENT_TYPES = {
    "asks_for_tool",
    "asks_for_link",
    "asks_for_tutorial",
    "shares_use_case",
    "expresses_pain",
    "expresses_skepticism",
    "tags_friend",
    "generic_hype",
    "creator_to_creator",
    "irrelevant",
}


@dataclass
class CommentSignal:
    id: str
    creator_id: str
    content_id: str | None = None
    comment_text: str = ""
    author_type_guess: str = "unknown"
    intent_type: str = "irrelevant"
    sentiment: str = "neutral"
    product_relevance: str = "low"
    extracted_need: str = ""
    extracted_objection: str = ""
    extracted_tool_mentions: list[str] = field(default_factory=list)
    confidence: float = 0.0

