from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable

from .models import Champion, Role


class ChampionDatabase:
    def __init__(self, champions: Dict[str, Champion]):
        self._champions = champions

    @classmethod
    def from_json(cls, path: str | Path) -> "ChampionDatabase":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        champions = {}
        for row in data["champions"]:
            champion = Champion(
                name=row["name"],
                cost=row["cost"],
                traits=row.get("traits", []),
                tier_priority=row.get("tier_priority", 3),
                roles=[Role(r) for r in row.get("roles", ["flex"])],
            )
            champions[champion.name.lower()] = champion
        return cls(champions)

    def get(self, name: str) -> Champion | None:
        return self._champions.get(name.lower())

    def __contains__(self, name: str) -> bool:
        return name.lower() in self._champions

    def names(self) -> Iterable[str]:
        return self._champions.keys()
