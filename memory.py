from __future__ import annotations
import json
import os
import time
from typing import Any, Dict, List

class Memory:
    """Append-only JSONL memory."""

    def __init__(self, path: str = "memory.jsonl") -> None:
        self.path = path
        if not os.path.exists(self.path):
            open(self.path, "a", encoding="utf-8").close()

    def store(self, **record: Any) -> None:
        rec = {"ts": time.time(), **record}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def all(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                out.append(json.loads(line))
        return out
