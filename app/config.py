from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

DEFAULT_PRODUCT_CONTEXT = (
    "An AI workspace that connects your apps so you can ask questions across "
    "your stack and turn answers into workflows."
)


def env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class AppConfig:
    notion_api_key: str = ""
    notion_tiktok_creators_database_id: str = ""
    notion_tiktok_waves_database_id: str = ""
    notion_tiktok_outreach_database_id: str = ""
    notion_sync_confirm: bool = False
    tiktok_official_api_enabled: bool = False
    tiktok_client_key: str = ""
    tiktok_client_secret: str = ""
    wavescout_offline_mode: bool = True
    wavescout_demo_mode: bool = True
    wavescout_allow_external_calls: bool = False
    wavescout_export_artifacts: bool = False
    data_dir: Path = DATA_DIR
    artifacts_dir: Path = ARTIFACTS_DIR


def load_config() -> AppConfig:
    return AppConfig(
        notion_api_key=os.getenv("NOTION_API_KEY", ""),
        notion_tiktok_creators_database_id=os.getenv("NOTION_TIKTOK_CREATORS_DATABASE_ID", ""),
        notion_tiktok_waves_database_id=os.getenv("NOTION_TIKTOK_WAVES_DATABASE_ID", ""),
        notion_tiktok_outreach_database_id=os.getenv("NOTION_TIKTOK_OUTREACH_DATABASE_ID", ""),
        notion_sync_confirm=env_bool("NOTION_SYNC_CONFIRM", False),
        tiktok_official_api_enabled=env_bool("TIKTOK_OFFICIAL_API_ENABLED", False),
        tiktok_client_key=os.getenv("TIKTOK_CLIENT_KEY", ""),
        tiktok_client_secret=os.getenv("TIKTOK_CLIENT_SECRET", ""),
        wavescout_offline_mode=env_bool("WAVESCOUT_OFFLINE_MODE", True),
        wavescout_demo_mode=env_bool("WAVESCOUT_DEMO_MODE", True),
        wavescout_allow_external_calls=env_bool("WAVESCOUT_ALLOW_EXTERNAL_CALLS", False),
        wavescout_export_artifacts=env_bool("WAVESCOUT_EXPORT_ARTIFACTS", False),
    )

