from __future__ import annotations
import time

class CircuitBreaker:
    """Simple circuit breaker."""

    def __init__(self, window: int = 5, cool: float = 5.0) -> None:
        self.window = window
        self.cool = cool
        self.fail = 0
        self.open = False
        self.opened_at = 0.0

    def record(self, success: bool) -> None:
        if self.open and (time.time() - self.opened_at) > self.cool:
            self.open = False
            self.fail = 0
        if success:
            self.fail = 0
            return
        self.fail += 1
        if self.fail >= self.window:
            self.open = True
            self.opened_at = time.time()
