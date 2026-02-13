from __future__ import annotations

import argparse

from autobuy import (
    AutoBuyController,
    AutoClickEngine,
    ChampionDatabase,
    ClickConfig,
    DecisionEngine,
    GameState,
    ShopFrame,
    ShopRecognitionEngine,
    ShopSlot,
    StrategyMode,
)


def build_demo_frame() -> ShopFrame:
    return ShopFrame(
        detected_slots=[
            ShopSlot(0, "Vayne", (400, 840, 140, 140), 0.96),
            ShopSlot(1, "Riven", (560, 840, 140, 140), 0.92),
            ShopSlot(2, "Morgana", (720, 840, 140, 140), 0.88),
            ShopSlot(3, "Ashe", (880, 840, 140, 140), 0.90),
            ShopSlot(4, "Garen", (1040, 840, 140, 140), 0.94),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="TFT AutoBuy prototype")
    parser.add_argument("--db", default="config/champions.sample.json")
    parser.add_argument("--strategy", choices=[s.value for s in StrategyMode], default=StrategyMode.SLOW_ROLL.value)
    parser.add_argument("--gold", type=int, default=34)
    parser.add_argument("--level", type=int, default=7)
    parser.add_argument("--live-click", action="store_true", help="Enable real mouse clicks via pyautogui")
    args = parser.parse_args()

    db = ChampionDatabase.from_json(args.db)
    recognizer = ShopRecognitionEngine()
    decider = DecisionEngine(db)
    clicker = AutoClickEngine(ClickConfig(dry_run=not args.live_click))

    controller = AutoBuyController(recognizer, decider, clicker)
    state = GameState(
        gold=args.gold,
        level=args.level,
        strategy=StrategyMode(args.strategy),
        bench_counts={"Vayne": 6, "Riven": 2},
        contested_units=["Ashe"],
    )

    for line in controller.run_scan(build_demo_frame(), state):
        print(line)

    print("---")
    print(f"scans={controller.stats.scan_count} purchases={controller.stats.purchase_count}")


if __name__ == "__main__":
    main()
