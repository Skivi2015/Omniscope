OmniScope Agents
================

Purpose
-------
Modular agent framework with tool registry, hot-reloadable skills, UCB1 exploration, retries, circuit breaker, multiprocessing, and a FastAPI server. Firebase wrapper provided.

Quick start
-----------
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python repo_pack.py --init
uvicorn server:app --reload --port 8080

Cloud Run
---------
export PROJECT_ID=your-project
gcloud builds submit --tag gcr.io/$PROJECT_ID/omniscope
gcloud run deploy omniscope --image gcr.io/$PROJECT_ID/omniscope --platform managed --allow-unauthenticated

Firebase
--------
cd functions && npm i && npm run build
Set env: firebase functions:config:set run.url="https://<cloud-run-url>"
firebase deploy --only functions,hosting

PyPI Release
------------
On GitHub Release "published", CI builds the package and publishes to PyPI using Trusted Publishing. See .github/workflows/pypi-publish.yml.