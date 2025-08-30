#!/bin/bash
set -e

echo "🔥 Firebase Functions Deployment Script"

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Install it with: npm install -g firebase-tools"
    exit 1
fi

# Check if we're in the functions directory or project root
if [[ ! -f "firebase.json" ]]; then
    echo "❌ firebase.json not found. Run this script from the project root."
    exit 1
fi

# Build the TypeScript functions
echo "📦 Building Firebase Functions..."
cd functions
npm install
npm run build
cd ..

# Set environment variables (optional - can be done manually)
if [[ -n "$CLOUD_RUN_URL" ]]; then
    echo "🔧 Setting Cloud Run URL configuration..."
    firebase functions:config:set run.url="$CLOUD_RUN_URL"
fi

# Deploy functions and hosting
echo "🚀 Deploying to Firebase..."
firebase deploy --only functions,hosting

echo "✅ Deployment complete!"
echo "📝 To set the Cloud Run URL later, run:"
echo "   firebase functions:config:set run.url=\"https://your-cloud-run-url\""