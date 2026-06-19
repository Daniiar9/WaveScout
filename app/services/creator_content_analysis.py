from __future__ import annotations

from collections import Counter

from app.models import CreatorCandidate, CreatorContentSample
from app.services.text import unique_keep_order


def summarize_creator_content(
    creator: CreatorCandidate,
    content_samples: list[CreatorContentSample],
) -> dict:
    themes = extract_content_themes(content_samples)
    formats = identify_creator_formats(content_samples)
    trust = assess_creator_trust_and_clarity(content_samples)
    summary = (
        f"{creator.handle} posts about {', '.join(themes[:4])}."
        if themes
        else f"{creator.handle} has limited imported content."
    )
    return {
        "creator_id": creator.id,
        "summary": summary,
        "themes": themes,
        "formats": formats,
        "trust_and_clarity": trust,
        "sample_count": len(content_samples),
        "natural_format": formats[0] if formats else "unknown",
    }


def extract_content_themes(content_samples: list[CreatorContentSample]) -> list[str]:
    values: list[str] = []
    for sample in content_samples:
        values.extend(sample.topics)
        values.extend(tag.lstrip("#") for tag in sample.hashtags)
        for phrase in ["AI workspace", "SaaS stack", "automation", "agents", "CRM", "Notion", "Slack"]:
            if phrase.lower() in sample.transcript_or_summary.lower() or phrase.lower() in sample.title_or_caption.lower():
                values.append(phrase)
    return unique_keep_order(values, 10)


def assess_creator_trust_and_clarity(content_samples: list[CreatorContentSample]) -> dict:
    if not content_samples:
        return {
            "score": 0,
            "clarity": "unknown",
            "specificity": "unknown",
            "demo_ability": "unknown",
            "hype_level": "unknown",
            "notes": "No content samples imported.",
        }
    combined = " ".join(f"{item.title_or_caption} {item.transcript_or_summary}" for item in content_samples).lower()
    format_bonus = sum(1 for item in content_samples if item.format in {"demo", "tutorial", "teardown", "comparison"})
    concrete_terms = sum(1 for term in ["example", "workflow", "crm", "notion", "slack", "setup", "how", "demo"] if term in combined)
    hype_terms = sum(1 for term in ["insane", "secret", "replace everyone", "100x", "guaranteed"] if term in combined)
    score = min(15, 5 + format_bonus * 2 + concrete_terms - hype_terms * 2)
    return {
        "score": max(0, score),
        "clarity": "high" if score >= 12 else "medium" if score >= 7 else "low",
        "specificity": "high" if concrete_terms >= 4 else "medium" if concrete_terms >= 2 else "low",
        "demo_ability": "high" if format_bonus >= 2 else "medium" if format_bonus == 1 else "low",
        "hype_level": "high" if hype_terms >= 2 else "medium" if hype_terms == 1 else "low",
        "notes": "Assessed from imported summaries only.",
    }


def identify_creator_formats(content_samples: list[CreatorContentSample]) -> list[str]:
    return [item for item, _count in Counter(sample.format for sample in content_samples).most_common()]

