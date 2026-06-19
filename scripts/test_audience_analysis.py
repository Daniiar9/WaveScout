from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from app.services.audience_analysis import infer_audience_profile
from app.services.comment_intelligence import extract_comment_signals
from app.services.storage import LocalJSONStorage


def main() -> None:
    storage = LocalJSONStorage()
    creator = storage.find_creator("@agentbuilderdaily")
    low_creator = storage.find_creator("@randomfitnesscreator")
    assert creator and low_creator
    profile = infer_audience_profile(
        creator,
        storage.content_for_creator(creator.id),
        extract_comment_signals(storage.comments_for_creator(creator.id), creator.id),
        DEFAULT_PRODUCT_CONTEXT,
    )
    assert {"founders", "builders", "RevOps/operators"} & set(profile.likely_audience_segments)
    assert profile.audience_quality_level == "high_intent"
    assert profile.audience_fit_score >= 70
    low_profile = infer_audience_profile(
        low_creator,
        storage.content_for_creator(low_creator.id),
        extract_comment_signals(storage.comments_for_creator(low_creator.id), low_creator.id),
        DEFAULT_PRODUCT_CONTEXT,
    )
    assert low_profile.audience_quality_level in {"low_quality", "irrelevant"}
    print("test_audience_analysis passed")


if __name__ == "__main__":
    main()

