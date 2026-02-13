from autobuy.database import ChampionDatabase
from autobuy.decision_engine import DecisionEngine
from autobuy.models import GameState, ShopSlot, StrategyMode


def test_close_to_three_star_scores_high():
    db = ChampionDatabase.from_json("config/champions.sample.json")
    engine = DecisionEngine(db)
    state = GameState(gold=30, level=7, strategy=StrategyMode.SLOW_ROLL, bench_counts={"Vayne": 6})
    decision = engine.evaluate_slot(ShopSlot(0, "Vayne", (0, 0, 10, 10), 1.0), state)
    assert decision.should_buy is True
    assert decision.score > 80


def test_low_gold_blocks_non_core():
    db = ChampionDatabase.from_json("config/champions.sample.json")
    engine = DecisionEngine(db)
    state = GameState(gold=10, level=7, strategy=StrategyMode.SLOW_ROLL)
    decision = engine.evaluate_slot(ShopSlot(0, "Morgana", (0, 0, 10, 10), 1.0), state)
    assert decision.should_buy is False
