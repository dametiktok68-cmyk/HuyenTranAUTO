from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .models import ShopSlot


@dataclass(slots=True)
class ShopFrame:
    """A normalized frame payload for recognition input.

    In production this should contain a screenshot ndarray.
    For now we support mocked slots so the rest of the system can be tested.
    """

    detected_slots: List[ShopSlot]


class ShopRecognitionEngine:
    def detect(self, frame: ShopFrame) -> list[ShopSlot]:
        # Placeholder for template/feature matching pipeline.
        return frame.detected_slots
