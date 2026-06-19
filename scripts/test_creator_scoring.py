from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.config import DEFAULT_PRODUCT_CONTEXT
from app.services.comment_intelligence import extract_comment_signals
from app.services.creator_scoring import score_creator_for_wave
from app.services.storage import LocalJSONStorage


def score(handle: str):
    storage = LocalJSONStorage()
    creator = storage.find_creator(handle)
    wave = storage.find_wave("Talk to your apps")
    assert creator and wave
    content = storage.content_for_creator(creator.id)
    signals = extract_comment_signals(storage.comments_for_creator(creator.id), creator.id)
    return score_creator_for_wave(creator, wave, content, signals, DEFAULT_PRODUCT_CONTEXT)


def main() -> None:
    high = score("@agentbuilderdaily")
    fitness = score("@randomfitnesscreator")
    generic = score("@genericchatgpttips")
    assert high.fit_level == "high"
    assert high.score >= 75
    assert fitness.fit_level == "reject"
    assert fitness.score < high.score
    assert generic.fit_level in {"low", "reject"}
    assert generic.score < high.score, "Follower count alone must not dominate score."
    print("test_creator_scoring passed")


if __name__ == "__main__":
    main()

