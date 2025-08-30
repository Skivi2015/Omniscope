#!/bin/bash
# Start script for OmniScope

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run install-chromebook.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if required files exist
if [ ! -f "server.py" ]; then
    echo "Initializing OmniScope..."
    python repo_pack.py --init
fi

# Start the server
echo "Starting OmniScope server..."
echo "Server will be available at: http://localhost:8080"
echo "Press Ctrl+C to stop the server"
uvicorn server:app --reload --port 8080