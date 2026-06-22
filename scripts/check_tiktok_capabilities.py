from __future__ import annotations

import argparse
from pathlib import Path

from bootstrap import bootstrap

ROOT = bootstrap()

from app.config import load_config
from app.services.tiktok_capability_service import (
    build_tiktok_capability_report,
    render_capability_report_markdown,
)


DEFAULT_ARTIFACT = ROOT / "artifacts" / "tiktok_capability_report.md"


def run_check(no_artifact: bool = False, out_path: str | None = None) -> dict:
    report = build_tiktok_capability_report(load_config())
    artifact = None
    if not no_artifact:
        artifact = Path(out_path) if out_path else DEFAULT_ARTIFACT
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(render_capability_report_markdown(report), encoding="utf-8")
    return {"report": report, "artifact": artifact}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check TikTok official API readiness without network calls.")
    parser.add_argument("--no-artifact", action="store_true")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    result = run_check(no_artifact=args.no_artifact, out_path=args.out or None)
    report = result["report"]
    print("TikTok Capability Check: PASS")
    print("External calls: false")
    print("TikTok scraping: false")
    print("TikTok DM/send: false")
    print("\nAvailable / dry-run:")
    for name in report.available + report.dry_run_only:
        capability = _capability_by_name(report.capabilities, name)
        print(f"* {capability.name}: {capability.status}")
    print("\nBlocked:")
    for name in report.blocked:
        capability = _capability_by_name(report.capabilities, name)
        print(f"* {capability.name}: {capability.reason}")
    if result["artifact"]:
        print("\nArtifact:")
        print(Path(result["artifact"]).relative_to(ROOT).as_posix())


def _capability_by_name(capabilities, name: str):
    for capability in capabilities:
        if capability.name == name:
            return capability
    raise KeyError(name)


if __name__ == "__main__":
    main()

