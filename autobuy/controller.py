from __future__ import annotations

from .click_engine import AutoClickEngine
from .decision_engine import DecisionEngine
from .models import GameState, ScanStats
from .recognition import ShopFrame, ShopRecognitionEngine


class AutoBuyController:
    def __init__(self, recognizer: ShopRecognitionEngine, decider: DecisionEngine, clicker: AutoClickEngine):
        self.recognizer = recognizer
        self.decider = decider
        self.clicker = clicker
        self.stats = ScanStats()

    def run_scan(self, frame: ShopFrame, state: GameState) -> list[str]:
        slots = self.recognizer.detect(frame)
        decisions = self.decider.pick_purchases(slots, state)
        slot_map = {s.index: s for s in slots}

        logs: list[str] = []
        self.stats.scan_count += 1

        for decision in decisions:
            ok = self.clicker.execute(decision, slot_map)
            status = "BUY" if ok else "SKIP"
            logs.append(f"[{status}] slot={decision.slot_index} champ={decision.champion_name} score={decision.score} ({decision.reason})")
            self.stats.last_detection = decision.champion_name
            self.stats.last_confidence = slot_map[decision.slot_index].confidence
            if ok:
                self.stats.purchase_count += 1

        return logs
