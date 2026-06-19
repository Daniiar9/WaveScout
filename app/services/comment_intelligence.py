from __future__ import annotations

import re
from collections import Counter

from app.models import CommentSignal
from app.services.text import stable_id, top_items, unique_keep_order

TOOL_NAMES = [
    "Notion",
    "Slack",
    "HubSpot",
    "Salesforce",
    "CRM",
    "Linear",
    "Jira",
    "Gmail",
    "Google Drive",
    "Zapier",
    "Airtable",
    "Asana",
]

BUYER_INTENTS = {
    "asks_for_tool",
    "asks_for_link",
    "asks_for_tutorial",
    "shares_use_case",
    "expresses_pain",
}


def classify_comment(comment_text: str) -> dict:
    text = comment_text.strip()
    lower = text.lower()
    tools = extract_tool_mentions(text)
    intent_type = "irrelevant"
    sentiment = "neutral"
    relevance = "low"
    need = ""
    objection = ""
    confidence = 0.45

    generic_phrases = {"first", "ai is crazy", "bro what", "follow me", "chatgpt changed my life", "wow", "insane"}
    if any(phrase in lower for phrase in generic_phrases):
        intent_type = "generic_hype"
        sentiment = "positive" if "follow me" not in lower else "neutral"
        confidence = 0.8
    if re.search(r"(^|\s)@[a-z0-9._-]+", lower):
        intent_type = "tags_friend"
        confidence = max(confidence, 0.65)
    if any(phrase in lower for phrase in ["what tool", "tool is this", "what app", "which app", "connect to", "work with"]):
        intent_type = "asks_for_tool"
        relevance = "high"
        need = "Wants to identify or validate the tool/workflow."
        confidence = 0.9
    if any(phrase in lower for phrase in ["link", "where can i", "can i try", "beta", "waitlist"]):
        intent_type = "asks_for_link"
        relevance = "high"
        need = "Wants access or a link."
        confidence = 0.88
    if any(phrase in lower for phrase in ["tutorial", "walkthrough", "how do i", "how would this", "can you make a tutorial"]):
        intent_type = "asks_for_tutorial"
        relevance = "high"
        need = "Wants implementation help."
        confidence = 0.86
    if any(phrase in lower for phrase in ["for my", "my crm", "my team", "our agency", "small agency", "at work", "we need"]):
        intent_type = "shares_use_case"
        relevance = "high"
        need = text
        confidence = 0.88
    if any(phrase in lower for phrase in ["too many", "scattered", "manual", "pain", "tired of", "need this", "annoying"]):
        intent_type = "expresses_pain"
        relevance = "high"
        need = text
        confidence = 0.86
    if any(phrase in lower for phrase in ["is this real", "just a demo", "fake", "actually work", "too good", "skeptical"]):
        intent_type = "expresses_skepticism"
        sentiment = "skeptical"
        relevance = "medium"
        objection = text
        confidence = 0.85
    if any(phrase in lower for phrase in ["duet", "collab", "creator meetup"]):
        intent_type = "creator_to_creator"
        relevance = "low"
        confidence = 0.65

    if tools and intent_type in {"irrelevant", "generic_hype"}:
        intent_type = "asks_for_tool"
        relevance = "high"
        need = "Mentions a concrete tool or workflow."
        confidence = 0.78

    if intent_type in BUYER_INTENTS and sentiment == "neutral":
        sentiment = "positive"

    return {
        "intent_type": intent_type,
        "sentiment": sentiment,
        "product_relevance": relevance,
        "extracted_need": need,
        "extracted_objection": objection,
        "extracted_tool_mentions": tools,
        "confidence": confidence,
    }


def extract_comment_signals(
    comments: list[str | dict],
    creator_id: str,
    content_id: str | None = None,
) -> list[CommentSignal]:
    signals: list[CommentSignal] = []
    for index, comment in enumerate(comments):
        if isinstance(comment, dict):
            text = str(comment.get("comment_text", ""))
            comment_content_id = comment.get("content_id") or content_id
            signal_id = comment.get("id") or stable_id("comment", creator_id, comment_content_id, text, index)
        else:
            text = str(comment)
            comment_content_id = content_id
            signal_id = stable_id("comment", creator_id, comment_content_id, text, index)
        classified = classify_comment(text)
        signals.append(
            CommentSignal(
                id=signal_id,
                creator_id=creator_id,
                content_id=comment_content_id,
                comment_text=text,
                author_type_guess="audience",
                **classified,
            )
        )
    return signals


def summarize_comment_intelligence(comment_signals: list[CommentSignal]) -> dict:
    intent_counts = Counter(signal.intent_type for signal in comment_signals)
    buyer_intent_count = sum(intent_counts[intent] for intent in BUYER_INTENTS)
    low_quality_count = intent_counts["generic_hype"] + intent_counts["irrelevant"] + intent_counts["tags_friend"]
    questions = [
        signal.comment_text
        for signal in comment_signals
        if "?" in signal.comment_text or signal.intent_type in {"asks_for_tool", "asks_for_tutorial", "asks_for_link"}
    ]
    pains = [
        signal.extracted_need or signal.comment_text
        for signal in comment_signals
        if signal.intent_type in {"expresses_pain", "shares_use_case"}
    ]
    objections = [
        signal.extracted_objection
        for signal in comment_signals
        if signal.extracted_objection or signal.intent_type == "expresses_skepticism"
    ]
    tool_mentions = unique_keep_order(
        tool for signal in comment_signals for tool in signal.extracted_tool_mentions
    )
    quality = _quality_label(comment_signals, buyer_intent_count, low_quality_count)
    if quality == "high":
        summary = "Audience is asking implementation-level questions, not just reacting to AI hype."
    elif quality == "medium":
        summary = "Audience shows useful awareness with some concrete questions mixed with lighter reactions."
    elif quality == "low":
        summary = "Comments are mostly generic hype or low-context reactions."
    else:
        summary = "Not enough comments to infer audience intent confidently."
    return {
        "buyer_intent_count": buyer_intent_count,
        "low_quality_count": low_quality_count,
        "top_intent_types": top_items([signal.intent_type for signal in comment_signals]),
        "common_pains": unique_keep_order(pains, 6),
        "common_questions": unique_keep_order(questions, 6),
        "objections": unique_keep_order([item for item in objections if item], 5),
        "tool_mentions": tool_mentions,
        "quality": quality,
        "summary": summary,
    }


def calculate_comment_intent_quality(comment_signals: list[CommentSignal]) -> int:
    if not comment_signals:
        return 0
    buyer = sum(1 for signal in comment_signals if signal.intent_type in BUYER_INTENTS)
    skeptical = sum(1 for signal in comment_signals if signal.intent_type == "expresses_skepticism")
    low_quality = sum(1 for signal in comment_signals if signal.intent_type in {"generic_hype", "irrelevant", "tags_friend"})
    raw = (buyer * 5) + (skeptical * 2) - (low_quality * 2)
    scaled = round(max(0, raw) / max(1, len(comment_signals) * 5) * 20)
    return min(20, scaled)


def extract_tool_mentions(text: str) -> list[str]:
    found: list[str] = []
    for tool in TOOL_NAMES:
        if re.search(rf"\b{re.escape(tool.lower())}\b", text.lower()):
            found.append(tool)
    return found


def _quality_label(signals: list[CommentSignal], buyer_intent_count: int, low_quality_count: int) -> str:
    if not signals:
        return "unknown"
    buyer_ratio = buyer_intent_count / len(signals)
    low_ratio = low_quality_count / len(signals)
    if buyer_intent_count >= 4 and buyer_ratio >= 0.5:
        return "high"
    if buyer_intent_count >= 2 and low_ratio < 0.6:
        return "medium"
    if low_ratio >= 0.6:
        return "low"
    return "mixed"

