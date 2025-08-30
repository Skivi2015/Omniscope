"""
Bootstrap to materialize the repo. Firebase-ready.
Run:
  python repo_pack.py --init
Then locally:
  uvicorn server:app --reload --port 8080
Cloud Run:
  docker build -t omniscope:latest . && docker run -p 8080:8080 omniscope
Firebase:
  cd functions && npm i && npm run build
  firebase emulators:start
"""
import os
import yaml

PACK = {
    "README.md": "OmniScope Agents\n================\n\nPurpose\n-------\nModular agent framework with tool registry, hot-reloadable skills, UCB1 exploration, retries, circuit breaker, multiprocessing, and a FastAPI server. Firebase wrapper provided.\n\nQuick start\n-----------\np...