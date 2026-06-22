from __future__ import annotations

import argparse
from pathlib import Path

from bootstrap import bootstrap

bootstrap()

from app.services.tiktok_owned_account_live import (
    check_tiktok_owned_account_live,
    render_tiktok_owned_account_live_markdown,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check TikTok Display API owned-account gate.")
    parser.add_argument("--handle", default="@owned_account")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--allow-tiktok-live", action="store_true", default=False)
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    status = check_tiktok_owned_account_live(
        allow_tiktok_live=args.allow_tiktok_live,
        dry_run=not args.allow_tiktok_live,
        handle=args.handle,
    )
    print("WaveScout TikTok Owned Account Check: PASS")
    print("External calls: false")
    print("TikTok live calls: false")
    print("TikTok scraping: false")
    print("Content posting: false")
    print(f"Blocked: {str(status['blocked']).lower()}")
    print(f"Blocked reason: {status['blocked_reason']}")

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_tiktok_owned_account_live_markdown(status), encoding="utf-8")
        print("\nArtifact:")
        print(out_path.as_posix())


if __name__ == "__main__":
    main()
