from __future__ import annotations
import re
import time
from typing import Any, Dict, List, Optional, Tuple
from memory import Memory
from tools import ToolRegistry, ToolError
from upgrade import SkillsReloader
from learning import UCB1
from health import CircuitBreaker

class Agent:
    """Adaptive agent with hot-reloaded skills and bandit tool selection."""

    def __init__(
        self,
        name: str,
        memory: Memory,
        tools: ToolRegistry,
        skills: SkillsReloader,
        max_steps: int = 8,
        retries: int = 2,
    ) -> None:
        self.name = name
        self.memory = memory
        self.tools = tools
        self.skills = skills
        self.max_steps = max_steps
        self.retries = retries
        self.bandit = UCB1()
        self.breakers: Dict[str, CircuitBreaker] = {}

    def _breaker(self, tool: str) -> CircuitBreaker:
        if tool not in self.breakers:
            self.breakers[tool] = CircuitBreaker()
        return self.breakers[tool]

    def plan(self, task: str) -> List[str]:
        parts = re.split(r"[.;\n]", task)
        steps = [p.strip() for p in parts if p.strip()]
        return steps or [task]

    def route(self, step: str) -> Tuple[str, Dict[str, Any]]:
        self.skills.refresh()
        rule = self.skills.match(step)
        if rule:
            return rule["prefer_tool"], rule.get("params", {})
        s = step.lower()
        if any(k in s for k in ("http://", "https://", "fetch")):
            return "http", {"method": "GET"}
        if any(k in s for k in ("python", "compute", "code")):
            return "python", {}
        if "json" in s:
            return "json", {}
        return "python", {}

    def solve(self, task: str) -> Dict[str, Any]:
        steps = self.plan(task)
        transcript: List[Dict[str, Any]] = []
        last_output: Any = None
        for step in steps[: self.max_steps]:
            tool_name, params = self.route(step)
            if self._breaker(tool_name).open:
                transcript.append({"step": step, "tool": tool_name, "skipped": True, "reason": "circuit_open"})
                continue
            weight = self.bandit.choose(tool_name)
            success = False
            error: Optional[str] = None
            out: Any = None
            for attempt in range(self.retries + 1):
                try:
                    out = self.tools.use(tool_name, step, context=last_output, **params)
                    success = True
                    break
                except ToolError as e:
                    error = str(e)
                    time.sleep(0.2 * (attempt + 1))
            self.bandit.update(tool_name, success)
            self._breaker(tool_name).record(success)
            rec = {"step": step, "tool": tool_name, "success": success, "weight": weight}
            if success:
                rec["output"] = out
                last_output = out
            else:
                rec["error"] = error
            transcript.append(rec)
            self.memory.store(task=task, step=step, tool=tool_name, success=success, output=out, error=error)
        return {"task": task, "result": last_output, "transcript": transcript}
