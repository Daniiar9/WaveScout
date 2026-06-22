from __future__ import annotations

import re
from urllib.parse import urlparse

from app.models import ProductIntelligenceBrief
from app.services.text import stable_id, unique_keep_order


def build_product_intelligence_from_text(product_text: str, product_url: str | None = None) -> ProductIntelligenceBrief:
    text = " ".join(product_text.split())
    category = infer_product_category(text)
    product_name = _infer_product_name(product_url, category)
    brief = ProductIntelligenceBrief(
        id=stable_id("product", product_url or "", text[:120]),
        product_url=product_url or "",
        product_name=product_name,
        one_liner=_one_liner(text, category),
        category=category,
        target_users=infer_target_users(text),
        target_buyers=infer_target_buyers(text),
        core_use_cases=infer_core_use_cases(text),
        pain_points=infer_pain_points(text),
        value_props=infer_value_props(text),
        differentiators=infer_differentiators(text),
        proof_points=infer_proof_points(text),
        competitors_or_alternatives=infer_competitors(text),
        trend_keywords=infer_trend_keywords(text),
        avoid_positioning=_avoid_positioning(text),
        confidence=0.82 if len(text) > 80 else 0.55,
        evidence=[f"Product text: {text[:220]}"],
    )
    brief.creator_relevant_angles = infer_creator_relevant_angles(brief)
    if product_url:
        brief.evidence.append(f"Product URL provided: {product_url}")
    return brief


def build_product_intelligence_from_url(product_url: str, allow_fetch: bool = False) -> ProductIntelligenceBrief:
    domain = urlparse(product_url).netloc or product_url
    status = (
        "URL fetch was not performed. Provide --product-text for full offline analysis."
        if not allow_fetch
        else "URL fetch is gated but live HTTP fetching is not implemented in this pass."
    )
    return ProductIntelligenceBrief(
        id=stable_id("product", product_url),
        product_url=product_url,
        product_name=domain.replace("www.", ""),
        one_liner=status,
        category="unknown",
        avoid_positioning=["Do not infer specific claims from URL alone.", "Do not fetch without explicit approval."],
        confidence=0.2,
        evidence=[status, f"Product URL provided: {product_url}"],
    )


def infer_product_category(text: str) -> str:
    lower = text.lower()
    if any(term in lower for term in ["workspace", "saas stack", "apps", "workflow", "notion", "slack", "crm"]):
        return "AI workspace / connected SaaS stack"
    if any(term in lower for term in ["agent", "automation", "automate"]):
        return "AI automation"
    if "developer" in lower or "code" in lower:
        return "developer tooling"
    return "startup software"


def infer_target_users(text: str) -> list[str]:
    lower = text.lower()
    users = []
    if any(term in lower for term in ["founder", "startup"]):
        users.append("founders")
    if any(term in lower for term in ["operator", "ops", "workflow", "crm", "revops"]):
        users.append("RevOps/operators")
    if any(term in lower for term in ["developer", "code", "api"]):
        users.append("developers")
    if any(term in lower for term in ["agency", "client"]):
        users.append("agency owners")
    users.extend(["AI builders", "SaaS teams"])
    return unique_keep_order(users, 6)


def infer_target_buyers(text: str) -> list[str]:
    lower = text.lower()
    buyers = ["founders", "operators"]
    if "sales" in lower or "crm" in lower:
        buyers.append("RevOps leaders")
    if "agency" in lower:
        buyers.append("agency owners")
    return unique_keep_order(buyers, 5)


def infer_core_use_cases(text: str) -> list[str]:
    lower = text.lower()
    use_cases = []
    if "ask" in lower and "apps" in lower:
        use_cases.append("Ask questions across connected apps")
    if "workflow" in lower:
        use_cases.append("Turn answers into workflows")
    if "crm" in lower:
        use_cases.append("Pull CRM context into decisions")
    if "slack" in lower or "notion" in lower:
        use_cases.append("Connect knowledge and communication tools")
    return unique_keep_order(use_cases or ["Explain and automate work across a software stack"], 6)


def infer_pain_points(text: str) -> list[str]:
    lower = text.lower()
    pains = ["Too many SaaS tabs", "Context scattered across tools"]
    if "workflow" in lower:
        pains.append("Manual workflow setup")
    if "questions" in lower or "ask" in lower:
        pains.append("Hard to answer business questions from disconnected app data")
    return unique_keep_order(pains, 6)


def infer_value_props(text: str) -> list[str]:
    props = ["One place to ask questions across the stack", "Turns scattered context into next actions"]
    if "workflow" in text.lower():
        props.append("Converts answers into workflows")
    return unique_keep_order(props, 5)


def infer_differentiators(text: str) -> list[str]:
    differentiators = []
    if "connects your apps" in text.lower():
        differentiators.append("Cross-app context instead of single-app AI")
    if "turn answers into workflows" in text.lower():
        differentiators.append("Moves from answer to action")
    return differentiators or ["Needs product-specific proof from source material"]


def infer_proof_points(text: str) -> list[str]:
    proof = []
    for tool in ["Notion", "Slack", "CRM", "HubSpot", "Gmail", "Linear"]:
        if tool.lower() in text.lower():
            proof.append(f"Mentions {tool} workflow context")
    return proof


def infer_competitors(text: str) -> list[str]:
    lower = text.lower()
    competitors = []
    for tool in ["zapier", "make", "notion ai", "chatgpt", "hubspot"]:
        if tool in lower:
            competitors.append(tool)
    return competitors


def infer_trend_keywords(text: str) -> list[str]:
    lower = text.lower()
    keywords = ["AI workspace", "talk to your apps", "connected SaaS stack", "workflow automation"]
    if "agent" in lower:
        keywords.append("AI agents")
    if "crm" in lower:
        keywords.append("RevOps automation")
    if "workflow" in lower:
        keywords.append("operator workflows")
    return unique_keep_order(keywords, 10)


def infer_creator_relevant_angles(product_brief: ProductIntelligenceBrief) -> list[str]:
    angles = [
        "Stop opening 12 SaaS tabs to answer one business question",
        "What if your SaaS stack had one brain?",
        "I asked my apps one question and got the workflow back",
    ]
    if "RevOps/operators" in product_brief.target_users:
        angles.append("Answering CRM questions from Slack and Notion context")
    if "agency owners" in product_brief.target_users:
        angles.append("How a small agency can connect client context without another dashboard")
    return unique_keep_order(angles, 6)


def render_product_brief_markdown(product_brief: ProductIntelligenceBrief) -> str:
    return f"""# Product Intelligence Brief

## Product
- Name: {product_brief.product_name}
- URL: {product_brief.product_url or "Not provided"}
- Category: {product_brief.category}
- One-liner: {product_brief.one_liner}
- Confidence: {product_brief.confidence}

## Target Users
{_bullets(product_brief.target_users)}

## Target Buyers
{_bullets(product_brief.target_buyers)}

## Core Use Cases
{_bullets(product_brief.core_use_cases)}

## Pain Points
{_bullets(product_brief.pain_points)}

## Value Props
{_bullets(product_brief.value_props)}

## Creator-Relevant Angles
{_bullets(product_brief.creator_relevant_angles)}

## Avoid Positioning
{_bullets(product_brief.avoid_positioning)}

## Evidence
{_bullets(product_brief.evidence)}
"""


def _one_liner(text: str, category: str) -> str:
    if text:
        stripped = re.sub(r"\s+", " ", text).strip()
        return stripped[:220]
    return f"A product in {category}."


def _infer_product_name(product_url: str | None, category: str) -> str:
    if not product_url:
        return category
    host = urlparse(product_url).netloc.replace("www.", "")
    return host or category


def _avoid_positioning(text: str) -> list[str]:
    return [
        "AI will replace everyone",
        "Fully automates the whole company",
        "Creator already uses the product",
        "Unsupported productivity claims",
    ]


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)

