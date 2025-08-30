from __future__ import annotations
import os
from typing import Any, Dict, Optional
import yaml

class SkillsReloader:
    """YAML skills hot-reloader."""

    def __init__(self, path: str) -> None:
        self.path = path
        self._mtime: float = 0.0
        self._doc: Dict[str, Any] = {"rules": []}
        self.refresh(force=True)

    def refresh(self, force: bool = False) -> None:
        try:
            m = os.path.getmtime(self.path)
        except OSError:
            return
        if force or m > self._mtime:
            with open(self.path, "r", encoding="utf-8") as f:
                self._doc = yaml.safe_load(f) or {"rules": []}
            self._mtime = m

    def match(self, text: str) -> Optional[Dict[str, Any]]:
        t = text.lower()
        for rule in self._doc.get("rules", []):
            terms = [str(x).lower() for x in rule.get("if_contains", [])]
            if any(term in t for term in terms):
                return rule
        return None
