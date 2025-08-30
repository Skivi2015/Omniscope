from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from typing import Any, Dict, Callable, Optional
import urllib.request

class ToolError(RuntimeError):
    pass

@dataclass
class Tool:
    name: str
    run: Callable[..., Any]

class ToolRegistry:
    """Registry of simple, auditable tools."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}
        self.register("python", self._python_exec)
        self.register("http", self._http_simple)
        self.register("json", self._json_tool)

    def register(self, name: str, func: Callable[..., Any]) -> None:
        self._tools[name] = Tool(name, func)

    def use(self, name: str, step: str, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise ToolError(f"unknown tool: {name}")
        try:
            return self._tools[name].run(step=step, **kwargs)
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(str(e))

    def _python_exec(self, step: str, timeout: int = 3, context: Optional[Any] = None) -> str:
        code = step
        s = step.lower()
        if "python" in s:
            code = step.split(step[s.find("python") :].split()[0], 1)[1].strip() or step
        wrapped = textwrap.dedent(
            f"""
import math, json, sys
_ctx = {json.dumps(context) if context is not None else 'None'}
{code}
print(locals().get('result') if 'result' in locals() else '')
"""
        )
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "prog.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write(wrapped)
            try:
                proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                raise ToolError("python timeout")
            if proc.returncode != 0:
                raise ToolError(proc.stderr.strip() or "python error")
            return proc.stdout.strip()

    def _http_simple(self, step: str, method: str = "GET", timeout: int = 10, context: Optional[Any] = None) -> str:
        tokens = step.split()
        url = next((t for t in tokens if t.startswith("http://") or t.startswith("https://")), None)
        if not url:
            raise ToolError("no url found")
        req = urllib.request.Request(url=url, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()[:100_000]
                return body.decode("utf-8", errors="ignore")
        except Exception as e:
            raise ToolError(f"http error: {e}")

    def _json_tool(self, step: str, context: Optional[Any] = None) -> str:
        try:
            payload = context if isinstance(context, str) and context.strip().startswith("{") else step
            data = json.loads(payload)
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ToolError(f"json error: {e}")
