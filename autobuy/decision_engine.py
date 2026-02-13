from __future__ import annotations

from .database import ChampionDatabase
from .models import CandidateDecision, GameState, Role, ShopSlot, StrategyMode


class DecisionEngine:
    def __init__(self, db: ChampionDatabase, min_score_to_buy: float = 45.0):
        self.db = db
        self.min_score_to_buy = min_score_to_buy

    def evaluate_slot(self, slot: ShopSlot, state: GameState) -> CandidateDecision:
        champion = self.db.get(slot.champion_name)
        if champion is None:
            return CandidateDecision(slot.index, slot.champion_name, 0.0, "not in target db", False)

        score = 20.0
        reasons: list[str] = []

        # Core role priority
        if Role.CORE in champion.roles:
            score += 22
            reasons.append("core")
        elif Role.CARRY in champion.roles:
            score += 14
            reasons.append("carry")

        # Base tier preference (1 high -> 5 low)
        score += max(0, (6 - champion.tier_priority) * 6)

        copies = state.copies_of(champion.name)

        # Star-up pressure system
        if copies >= 6:
            score += 30
            reasons.append("close to 3-star")
        elif copies >= 3:
            score += 18
            reasons.append("close to 2-star")
        elif copies >= 1:
            score += 6

        # Econ / strategy behavior
        if state.gold < 20 and Role.CORE not in champion.roles:
            score -= 28
            reasons.append("low gold conserve")
        elif state.gold >= 50:
            score += 10
            reasons.append("high econ")

        if state.strategy == StrategyMode.SLOW_ROLL and champion.cost in (2, 3):
            score += 12
            reasons.append("slow roll cost target")
        if state.strategy == StrategyMode.FAST_8 and champion.cost >= 4:
            score += 14
            reasons.append("fast 8 high cost")
        if state.strategy == StrategyMode.REROLL and champion.cost <= 3:
            score += 8
            reasons.append("reroll low cost")

        # Roll timing by level
        if state.level == 7 and champion.cost == 3:
            score += 10
            reasons.append("lvl7 3-cost spike")

        # Contested penalty
        if champion.name in state.contested_units:
            score -= 14
            reasons.append("contested")

        # Detection confidence
        score *= slot.confidence

        should_buy = score >= self.min_score_to_buy
        reason = ", ".join(reasons) if reasons else "baseline"

        return CandidateDecision(slot.index, champion.name, round(score, 2), reason, should_buy)

    def pick_purchases(self, slots: list[ShopSlot], state: GameState) -> list[CandidateDecision]:
        decisions = [self.evaluate_slot(slot, state) for slot in slots]
        decisions.sort(key=lambda d: d.score, reverse=True)
        return [d for d in decisions if d.should_buy]
