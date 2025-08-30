#!/bin/bash
# Chromebook Installation Script for OmniScope
# This script automates the installation process for Chromebook users

echo "OmniScope Chromebook Installation Script"
echo "========================================"

# Check if we're running in a Linux environment
if ! command -v apt &> /dev/null; then
    echo "Error: This script requires a Linux environment."
    echo "Please enable Linux (Beta) on your Chromebook first:"
    echo "1. Go to Settings → Advanced → Developers"
    echo "2. Turn on 'Linux development environment (Beta)'"
    echo "3. Follow the setup wizard"
    exit 1
fi

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "Installing Python 3, pip, venv, and git..."
sudo apt install python3 python3-pip python3-venv git -y

# Check if we're already in the OmniScope directory
if [ ! -f "requirements.txt" ]; then
    # Clone the repository if not already here
    echo "Cloning OmniScope repository..."
    git clone https://github.com/Skivi2015/Omniscope.git
    cd Omniscope
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize the repository
echo "Initializing OmniScope..."
python repo_pack.py --init

echo ""
echo "Installation complete!"
echo "====================="
echo ""
echo "To start OmniScope:"
echo "1. Navigate to the OmniScope directory"
echo "2. Activate the virtual environment: source .venv/bin/activate"
echo "3. Start the server: uvicorn server:app --reload --port 8080"
echo "4. Open Chrome and go to: http://localhost:8080"
echo ""
echo "Or run: ./start.sh"