from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class NotionSyncResult:
    ok: bool
    dry_run: bool
    target: str
    payload: dict
    message: str
    external_call_made: bool = False
    missing_database_ids: list[str] = field(default_factory=list)

