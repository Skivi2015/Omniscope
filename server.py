# FastAPI server for OmniScope
from fastapi import FastAPI, Request
from agent import AGENTS
app = FastAPI()
@app.post('/solve')
async def solve(request: Request):
    data = await request.json()
    bot = data.get('bot')
    task = data.get('task')
    if bot in AGENTS:
        return AGENTS[bot].act(task)
    return {'error': 'bot not found'}
