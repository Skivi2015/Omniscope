from __future__ import annotations
import math
from typing import Dict

class UCB1:
    """Per-arm UCB1 bandit."""

    def __init__(self) -> None:
        self.counts: Dict[str, int] = {}
        self.rewards: Dict[str, float] = {}
        self.total: int = 0

    def choose(self, arm: str) -> float:
        self.total += 1
        self.counts.setdefault(arm, 0)
        self.rewards.setdefault(arm, 0.0)
        c = self.counts[arm]
        if c == 0:
            self.counts[arm] = 1
            return 1000.0  # Large value instead of infinity
        bonus = math.sqrt(2.0 * math.log(self.total) / c)
        return self.rewards[arm] / c + bonus

    def update(self, arm: str, success: bool) -> None:
        self.counts[arm] = self.counts.get(arm, 0) + 1
        self.rewards[arm] = self.rewards.get(arm, 0.0) + (1.0 if success else 0.0)
