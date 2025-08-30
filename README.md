OmniScope Agents
================

Purpose
-------
Modular agent framework with tool registry, hot-reloadable skills, UCB1 exploration, retries, circuit breaker, multiprocessing, and a FastAPI server. Firebase wrapper provided.

Quick start
-----------
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python repo_pack.py --init
uvicorn server:app --reload --port 8080
```

Test the API:
```bash
curl -X POST "http://localhost:8080/solve" \
  -H "Content-Type: application/json" \
  -d '{"bot": "seomi", "task": "python result = 2 + 2"}'
```

Available Bots
--------------
- **seomi**: SEO content helper
- **soshie**: Social media helper  
- **scouty**: Ops helper
- **Cookie**: Real-time trading agent
- **Rusty**: Social media automation
- **Browny**: Playful analyst

Cloud Run Deployment
-------------------
```bash
# Set your project ID
export PROJECT_ID=your-gcp-project-id

# Deploy using the script
./deploy-cloud-run.sh

# Or manually:
gcloud builds submit --tag gcr.io/$PROJECT_ID/omniscope
gcloud run deploy omniscope \
  --image gcr.io/$PROJECT_ID/omniscope \
  --platform managed \
  --allow-unauthenticated
```

Firebase Deployment
------------------
```bash
# Set your project ID in .firebaserc
# Update Cloud Run URL after deploying to Cloud Run
export CLOUD_RUN_URL="https://your-cloud-run-url"

# Deploy using the script
./deploy-firebase.sh

# Or manually:
cd functions && npm i && npm run build && cd ..
firebase functions:config:set run.url="$CLOUD_RUN_URL"
firebase deploy --only functions,hosting
```

Architecture
-----------
- **Cloud Run**: Hosts the Python FastAPI server with all bot logic
- **Firebase Functions**: Provides a serverless proxy to Cloud Run  
- **Firebase Hosting**: Serves the web interface
- **GitHub Actions**: Automated CI/CD for Cloud Run deployments

The Firebase Function acts as a lightweight proxy that forwards requests to the Cloud Run service, providing a unified endpoint and additional Firebase integration capabilities.

Environment Variables
--------------------
**Cloud Run**:
- `PORT`: Server port (default: 8080)

**Firebase Functions**:
- `RUN_URL`: Cloud Run service URL (set via firebase functions:config:set)

Development
----------
```bash
# Run tests
python -m pytest tests/

# Local development
uvicorn server:app --reload --port 8080

# Firebase emulator
firebase emulators:start
```

PyPI Release
------------
On GitHub Release "published", CI builds the package and publishes to PyPI using Trusted Publishing. See .github/workflows/pypi-publish.yml.
