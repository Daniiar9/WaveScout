from __future__ import annotations

from bootstrap import bootstrap

bootstrap()

from app.mcp import server
from app.mcp.tools import TOOL_REGISTRY, list_trend_waves, run_wave_scout


def main() -> None:
    assert "run_wave_scout" in TOOL_REGISTRY
    assert "build_creator_intelligence_packet" in TOOL_REGISTRY
    waves = list_trend_waves()
    assert waves["trend_waves"]
    result = run_wave_scout("Talk to your apps", top=2)
    assert result["offline"] is True
    assert result["send_allowed"] is False
    assert len(result["top_packets"]) == 2
    assert hasattr(server, "create_server")
    print("test_mcp_tools_import passed")


if __name__ == "__main__":
    main()

