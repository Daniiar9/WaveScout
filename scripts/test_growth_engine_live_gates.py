from __future__ import annotations

import os

from bootstrap import bootstrap

bootstrap()

from app.services.growth_engine import run_growth_engine

PRODUCT_TEXT = "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows."


def main() -> None:
    brief = run_growth_engine(product_text=PRODUCT_TEXT, discovery_provider="exa")
    assert brief.safety_status["external_calls"] is False
    assert brief.safety_status["send_allowed"] is False
    assert brief.discovery_summary["selected_provider"] == "exa"
    assert brief.discovery_summary["live_discovery_status"]["external_calls"] is False

    old_allow = os.environ.get("WAVESCOUT_ALLOW_EXTERNAL_CALLS")
    old_exa = os.environ.get("EXA_API_KEY")
    try:
        os.environ["WAVESCOUT_ALLOW_EXTERNAL_CALLS"] = "true"
        os.environ.pop("EXA_API_KEY", None)
        blocked = run_growth_engine(
            product_text=PRODUCT_TEXT,
            discovery_provider="exa",
            allow_external_discovery=True,
        )
        reason = blocked.discovery_summary["live_discovery_status"]["blocked_reason"]
        assert "EXA_API_KEY" in reason
        assert blocked.discovery_summary["live_discovery_status"]["external_calls"] is False
    finally:
        _restore_env("WAVESCOUT_ALLOW_EXTERNAL_CALLS", old_allow)
        _restore_env("EXA_API_KEY", old_exa)
    print("test_growth_engine_live_gates passed")


def _restore_env(name: str, value: str | None) -> None:
    if value is None:
        os.environ.pop(name, None)
    else:
        os.environ[name] = value


if __name__ == "__main__":
    main()
