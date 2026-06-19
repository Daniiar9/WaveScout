from __future__ import annotations

from app.models import ContentAngle, CreatorCandidate, CreatorFitScore, CreatorProposal, TrendWave


def generate_creator_proposal(
    creator: CreatorCandidate,
    trend_wave: TrendWave,
    fit_score: CreatorFitScore,
    recommended_angle: ContentAngle,
    product_context: str,
) -> CreatorProposal:
    if fit_score.fit_level in {"low", "reject"}:
        return CreatorProposal(
            creator_id=creator.id,
            collaboration_angle=recommended_angle.title,
            suggested_video_angle=recommended_angle.title,
            approval_required=True,
            send_allowed=False,
            do_not_send_reason=(
                "Do not send: creator is not qualified enough for outreach based on imported evidence. "
                f"Fit level is {fit_score.fit_level}."
            ),
        )
    name = creator.display_name or creator.handle
    topic = _theme_phrase(creator)
    opening = f"Draft for {creator.handle}: {recommended_angle.title}"
    product_phrase = _lower_first(product_context).rstrip(".")
    angle = recommended_angle.title.strip()
    insight = fit_score.best_angle.rstrip(".")
    dm = (
        f"Hey - saw your videos around {topic}.\n\n"
        f"We're building in that lane: {product_phrase}.\n\n"
        f"The audience signal is practical: {insight}.\n\n"
        f"One native angle:\n\n\"{angle}\"\n\n"
        "Open to taking a look to see if it's worth a short demo?"
    )
    email = (
        f"Subject: Creator idea around {trend_wave.name}\n\n"
        f"Hey {name},\n\n"
        f"Saw your recent content around {topic}. We're building a tool in that lane: {product_phrase}.\n\n"
        f"The audience signal I noticed: {insight}.\n\n"
        f"One angle that could fit your format is: \"{angle}\"\n\n"
        "Would you be open to reviewing it and deciding whether it is worth a short demo? No pressure to post.\n\n"
        "Thanks."
    )
    return CreatorProposal(
        creator_id=creator.id,
        subject_or_opening=opening,
        dm_draft=dm,
        email_draft=email,
        collaboration_angle=recommended_angle.title,
        why_this_creator="; ".join(fit_score.reasons[:3]),
        suggested_video_angle=recommended_angle.title,
        approval_required=True,
        send_allowed=False,
        do_not_send_reason="Draft only. Human approval is required before any outreach.",
    )


def _lower_first(value: str) -> str:
    return value[:1].lower() + value[1:] if value else value


def _theme_phrase(creator: CreatorCandidate) -> str:
    themes = creator.categories[:2] or creator.hashtags_used[:2]
    if not themes:
        return "the creator-led AI workflow space"
    return ", ".join(theme.lstrip("#") for theme in themes)
