from __future__ import annotations

import re


def parse_tiktok_url(url: str) -> dict:
    """Parse TikTok URL strings without fetching or browser automation."""
    cleaned = url.strip()
    handle_match = re.search(r"@([A-Za-z0-9._-]+)", cleaned)
    video_match = re.search(r"/video/(\d+)", cleaned)
    return {
        "input": cleaned,
        "handle": f"@{handle_match.group(1)}" if handle_match else "",
        "video_id": video_match.group(1) if video_match else "",
        "is_tiktok_url": "tiktok.com" in cleaned.lower(),
        "fetched": False,
    }

