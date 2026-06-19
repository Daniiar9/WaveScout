from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from demo_tiktok_growth_workflow import run_demo


def main() -> None:
    result = run_demo()
    top = result["top_packets"]
    assert len(top) == 3
    assert top[0].fit_score.score >= top[1].fit_score.score
    assert any(packet.creator_candidate.handle == "@agentbuilderdaily" for packet in top)
    assert any(packet.creator_candidate.handle == "@aistackreview" for packet in top)
    assert any(packet.proposal_draft.dm_draft for packet in top if packet.fit_score.fit_level == "high")
    low = [packet for packet in result["all_packets"] if packet.creator_candidate.handle == "@randomfitnesscreator"][0]
    assert low.fit_score.fit_level == "reject"
    assert all(packet.send_allowed is False for packet in result["all_packets"])
    assert all(packet.approval_required is True for packet in result["all_packets"])
    assert result["external_calls_made"] is False
    print("test_tiktok_growth_workflow passed")


if __name__ == "__main__":
    main()

