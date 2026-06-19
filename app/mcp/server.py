from __future__ import annotations

from app.mcp.tools import TOOL_REGISTRY, register_tools


def create_server():
    fastmcp_cls = _load_fastmcp()
    if fastmcp_cls is None:
        return None
    server = fastmcp_cls("WaveScout")
    return register_tools(server)


def _load_fastmcp():
    try:
        from fastmcp import FastMCP

        return FastMCP
    except Exception:
        try:
            from mcp.server.fastmcp import FastMCP

            return FastMCP
        except Exception:
            return None


mcp = create_server()


def main() -> None:
    if mcp is None:
        print("FastMCP is not installed. Available WaveScout tools:")
        for name in TOOL_REGISTRY:
            print(f"- {name}")
        return
    mcp.run()


if __name__ == "__main__":
    main()

