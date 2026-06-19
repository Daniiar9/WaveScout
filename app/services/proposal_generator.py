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
    topic = ", ".join(creator.categories[:2]) if creator.categories else trend_wave.name
    opening = f"Draft for {creator.handle}: {recommended_angle.title}"
    product_phrase = _lower_first(product_context).rstrip(".")
    angle_sentence = _as_sentence(recommended_angle.title)
    dm = (
        f"Hey {name} - saw your videos around {topic}. We're building {product_phrase}, "
        f"which fits the wave you've been covering around {trend_wave.name}. "
        f"I had an angle that might work for your audience: {angle_sentence} "
        "Would you be open to taking a look?"
    )
    email = (
        f"Subject: Creator idea around {trend_wave.name}\n\n"
        f"Hey {name},\n\n"
        f"Saw your recent content around {topic}. We're building {product_phrase}. "
        f"The angle I think could fit your audience is: {angle_sentence}\n\n"
        "No pressure to post. Would you be open to reviewing the product and seeing whether the angle feels native to your content?\n\n"
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


def _as_sentence(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return ""
    if stripped[-1] in ".!?":
        return stripped
    return f"{stripped}."
