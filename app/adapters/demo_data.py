from __future__ import annotations

from app.services.storage import LocalJSONStorage


def load_demo_data() -> dict:
    storage = LocalJSONStorage()
    return {
        "waves": storage.load_waves(),
        "creators": storage.load_creators(),
        "content_samples": storage.load_content_samples(),
        "comments": storage.load_comments(),
    }

