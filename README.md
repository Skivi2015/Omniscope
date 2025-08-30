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

Chromebook Installation
----------------------
To install OmniScope on a Chromebook, you need to enable the Linux development environment:

### Prerequisites
1. **Enable Linux (Beta)** on your Chromebook:
   - Open Settings → Advanced → Developers
   - Turn on "Linux development environment (Beta)"
   - Follow the setup wizard to install Linux

### Easy Installation (Recommended)
```bash
# 1. Download and run the installation script
wget https://github.com/Skivi2015/Omniscope/raw/main/install-chromebook.sh
chmod +x install-chromebook.sh
./install-chromebook.sh

# 2. Start the server
./start.sh
```

### Manual Installation Steps
```bash
# 1. Update the system
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3 and pip (if not already installed)
sudo apt install python3 python3-pip python3-venv git -y

# 3. Clone the repository
git clone https://github.com/Skivi2015/Omniscope.git
cd Omniscope

# 4. Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Initialize the repository
python repo_pack.py --init

# 6. Start the server
uvicorn server:app --reload --port 8080
```

### Accessing the Application
- Open Chrome and navigate to `http://localhost:8080`
- The OmniScope API will be available for use

### Alternative Installation Methods for Chromebooks
- **Online IDE**: Use Replit, Codepen, or similar online Python environments
- **Android App**: If Android app support is enabled, try Python IDEs from Google Play Store
- **Docker**: If Docker is available in your Linux environment, use the provided Dockerfile

Cloud Run
---------
```bash
export PROJECT_ID=your-project
gcloud builds submit --tag gcr.io/$PROJECT_ID/omniscope
gcloud run deploy omniscope --image gcr.io/$PROJECT_ID/omniscope --platform managed --allow-unauthenticated
```

Firebase
--------
```bash
cd functions && npm i && npm run build
# Set env: firebase functions:config:set run.url="https://<cloud-run-url>"
firebase deploy --only functions,hosting
```

PyPI Release
------------
On GitHub Release "published", CI builds the package and publishes to PyPI using Trusted Publishing. See .github/workflows/pypi-publish.yml.
