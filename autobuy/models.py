from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class Role(str, Enum):
    CORE = "core"
    FLEX = "flex"
    CARRY = "carry"


class StrategyMode(str, Enum):
    SLOW_ROLL = "slow_roll"
    FAST_8 = "fast_8"
    REROLL = "reroll"
    FLEX = "flex"


@dataclass(slots=True)
class Champion:
    name: str
    cost: int
    traits: List[str]
    tier_priority: int
    roles: List[Role]


@dataclass(slots=True)
class ShopSlot:
    index: int
    champion_name: str
    bbox: tuple[int, int, int, int]
    confidence: float


@dataclass(slots=True)
class GameState:
    gold: int
    level: int
    strategy: StrategyMode = StrategyMode.FLEX
    board_counts: Dict[str, int] = field(default_factory=dict)
    bench_counts: Dict[str, int] = field(default_factory=dict)
    contested_units: List[str] = field(default_factory=list)

    def copies_of(self, name: str) -> int:
        return self.board_counts.get(name, 0) + self.bench_counts.get(name, 0)


@dataclass(slots=True)
class CandidateDecision:
    slot_index: int
    champion_name: str
    score: float
    reason: str
    should_buy: bool


@dataclass(slots=True)
class ScanStats:
    scan_count: int = 0
    purchase_count: int = 0
    last_detection: Optional[str] = None
    last_confidence: float = 0.0
