from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any, TypeVar

from app.config import DATA_DIR
from app.models import CommentSignal, CreatorCandidate, CreatorContentSample, TrendWave
from app.models.common import to_plain_dict

T = TypeVar("T")


class LocalJSONStorage:
    def __init__(self, data_dir: Path | str = DATA_DIR) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, filename: str) -> Path:
        return self.data_dir / filename

    def read_json(self, filename: str, default: Any = None) -> Any:
        path = self._path(filename)
        if not path.exists():
            return [] if default is None else default
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def write_json(self, filename: str, payload: Any) -> None:
        path = self._path(filename)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(to_plain_dict(payload), handle, indent=2, sort_keys=True)
            handle.write("\n")

    def load_waves(self) -> list[TrendWave]:
        return [coerce_dataclass(TrendWave, item) for item in self.read_json("demo_waves.json")]

    def load_creators(self) -> list[CreatorCandidate]:
        return [coerce_dataclass(CreatorCandidate, item) for item in self.read_json("demo_creators.json")]

    def load_content_samples(self) -> list[CreatorContentSample]:
        return [coerce_dataclass(CreatorContentSample, item) for item in self.read_json("demo_content_samples.json")]

    def load_comments(self) -> list[dict]:
        return self.read_json("demo_comments.json")

    def save_waves(self, waves: list[TrendWave]) -> None:
        self.write_json("demo_waves.json", waves)

    def save_creators(self, creators: list[CreatorCandidate]) -> None:
        self.write_json("demo_creators.json", creators)

    def save_content_samples(self, samples: list[CreatorContentSample]) -> None:
        self.write_json("demo_content_samples.json", samples)

    def save_comments(self, comments: list[dict]) -> None:
        self.write_json("demo_comments.json", comments)

    def find_wave(self, wave_name_or_id: str) -> TrendWave | None:
        needle = wave_name_or_id.strip().lower()
        for wave in self.load_waves():
            if wave.id.lower() == needle or wave.name.lower() == needle or needle in wave.name.lower():
                return wave
        return None

    def find_creator(self, handle_or_id: str) -> CreatorCandidate | None:
        needle = handle_or_id.strip().lower().lstrip("@")
        for creator in self.load_creators():
            if creator.id.lower() == needle or creator.handle.lower().lstrip("@") == needle:
                return creator
        return None

    def content_for_creator(self, creator_id: str) -> list[CreatorContentSample]:
        return [sample for sample in self.load_content_samples() if sample.creator_id == creator_id]

    def comments_for_creator(self, creator_id: str) -> list[dict]:
        return [comment for comment in self.load_comments() if comment.get("creator_id") == creator_id]


def coerce_dataclass(cls: type[T], payload: dict) -> T:
    if is_dataclass(cls):
        allowed = {field.name for field in fields(cls)}
        return cls(**{key: value for key, value in payload.items() if key in allowed})
    return cls(**payload)

