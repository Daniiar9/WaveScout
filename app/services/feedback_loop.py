from __future__ import annotations

from app.models import CreatorFitScore, PerformanceFeedback


def ingest_feedback_manual(feedback: PerformanceFeedback | dict) -> PerformanceFeedback:
    if isinstance(feedback, PerformanceFeedback):
        return feedback
    return PerformanceFeedback(**feedback)


def update_creator_score_with_feedback(score: CreatorFitScore, feedback: PerformanceFeedback) -> CreatorFitScore:
    lift = 0
    if feedback.creator_response.lower() in {"interested", "yes", "replied"}:
        lift += 3
    if feedback.signups > 0:
        lift += 5
    if feedback.clicks > 10:
        lift += 2
    score.score = min(100, score.score + lift)
    if lift:
        score.reasons.append(f"Manual feedback added positive signal (+{lift}).")
    return score


def summarize_feedback(feedback_items: list[PerformanceFeedback | dict]) -> dict:
    items = [ingest_feedback_manual(item) for item in feedback_items]
    return {
        "count": len(items),
        "total_views": sum(item.views for item in items),
        "total_likes": sum(item.likes for item in items),
        "total_comments": sum(item.comments for item in items),
        "total_clicks": sum(item.clicks for item in items),
        "total_signups": sum(item.signups for item in items),
        "interested_creators": [
            item.creator_handle
            for item in items
            if item.creator_response.lower() in {"interested", "yes", "replied"}
        ],
        "external_calls_made": False,
    }


def render_feedback_summary_markdown(feedback_items: list[PerformanceFeedback | dict]) -> str:
    summary = summarize_feedback(feedback_items)
    return f"""# Performance Feedback Summary

- Feedback items: {summary["count"]}
- Total views: {summary["total_views"]}
- Total likes: {summary["total_likes"]}
- Total comments: {summary["total_comments"]}
- Total clicks: {summary["total_clicks"]}
- Total signups: {summary["total_signups"]}
- Interested creators: {", ".join(summary["interested_creators"]) or "None"}
- External calls made: false
"""

