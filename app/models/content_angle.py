from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ContentAngle:
    id: str
    creator_id: str
    trend_wave_id: str
    title: str
    hook: str = ""
    short_script: str = ""
    why_it_fits_wave: str = ""
    product_mention_style: str = ""
    creator_prompt: str = ""
    avoid_saying: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    format: str = "demo"
    confidence: float = 0.0

