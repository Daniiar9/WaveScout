from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.models import CreatorFitScore, PerformanceFeedback
from app.services.feedback_loop import ingest_feedback_manual, render_feedback_summary_markdown, summarize_feedback, update_creator_score_with_feedback


def main() -> None:
    feedback = ingest_feedback_manual(
        {
            "creator_handle": "@creator",
            "content_angle": "Talk to your apps",
            "creator_response": "interested",
            "clicks": 12,
            "signups": 1,
        }
    )
    assert isinstance(feedback, PerformanceFeedback)
    summary = summarize_feedback([feedback])
    assert summary["external_calls_made"] is False
    assert summary["total_signups"] == 1
    score = CreatorFitScore(creator_id="creator", trend_wave_id="wave", score=70, fit_level="medium")
    updated = update_creator_score_with_feedback(score, feedback)
    assert updated.score > 70
    assert "External calls made: false" in render_feedback_summary_markdown([feedback])
    print("test_feedback_loop passed")


if __name__ == "__main__":
    main()

