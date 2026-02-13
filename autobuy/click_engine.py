from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .models import CandidateDecision, ShopSlot


@dataclass(slots=True)
class ClickConfig:
    human_delay_min: float = 0.06
    human_delay_max: float = 0.16
    dry_run: bool = True
    screen_width: int = 1920
    screen_height: int = 1080


class AutoClickEngine:
    def __init__(self, config: ClickConfig):
        self.config = config

    def _center(self, bbox: tuple[int, int, int, int]) -> tuple[int, int]:
        x, y, w, h = bbox
        return x + w // 2, y + h // 2

    def _safe(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        return 0 <= x <= self.config.screen_width and 0 <= y <= self.config.screen_height

    def execute(self, decision: CandidateDecision, slot_map: dict[int, ShopSlot]) -> bool:
        slot = slot_map[decision.slot_index]
        target = self._center(slot.bbox)
        if not self._safe(target):
            return False

        time.sleep(random.uniform(self.config.human_delay_min, self.config.human_delay_max))

        if self.config.dry_run:
            return True

        try:
            import pyautogui

            pyautogui.click(*target)
            return True
        except Exception:
            return False
