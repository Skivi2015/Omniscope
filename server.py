from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yaml
from scaling import build_agent

app = FastAPI(title="OmniScope API")

with open("bots.yaml", "r", encoding="utf-8") as f:
    BOTS = yaml.safe_load(f)["bots"]

class SolveReq(BaseModel):
    bot: str
    task: str

@app.post("/solve")
def solve(req: SolveReq):
    bot_cfg = BOTS.get(req.bot)
    if not bot_cfg:
        raise HTTPException(status_code=404, detail="unknown bot")
    agent = build_agent(req.bot, bot_cfg["skills_path"])
    return agent.solve(req.task)
