# FastAPI server for OmniScope
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from agent import AGENTS
import os

app = FastAPI()

# Serve static files from web directory
app.mount("/static", StaticFiles(directory="web"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('web/index.html')

@app.post('/solve')
async def solve(request: Request):
    data = await request.json()
    bot = data.get('bot')
    task = data.get('task')
    if bot in AGENTS:
        return AGENTS[bot].act(task)
    return {'error': 'bot not found'}
