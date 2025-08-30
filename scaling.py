from __future__ import annotations
from typing import Any, Dict, List
from agent import Agent
from memory import Memory
from tools import ToolRegistry
from upgrade import SkillsReloader

def build_agent(bot: str, skills_path: str) -> Agent:
    mem = Memory(path=f"memory_{bot}.jsonl")
    tools = ToolRegistry()
    skills = SkillsReloader(skills_path)
    return Agent(name=bot, memory=mem, tools=tools, skills=skills)