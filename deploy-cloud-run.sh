#!/bin/bash
set -e

echo "☁️ Cloud Run Deployment Script"

# Configuration (can be overridden with environment variables)
PROJECT_ID=${PROJECT_ID:-"your-project-id"}
SERVICE_NAME=${SERVICE_NAME:-"omniscope"}
REGION=${REGION:-"us-central1"}

if [[ "$PROJECT_ID" == "your-project-id" ]]; then
    echo "❌ Please set your PROJECT_ID environment variable"
    echo "   export PROJECT_ID=your-actual-project-id"
    exit 1
fi

# Check if gcloud is installed and configured
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if Docker is available (for local testing)
if command -v docker &> /dev/null; then
    echo "🐳 Building and testing locally first..."
    docker build -t $SERVICE_NAME:latest .
    echo "✅ Local Docker build successful"
fi

# Set the current project
echo "🔧 Setting gcloud project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Build and submit to Cloud Build
echo "📦 Building with Cloud Build..."
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"
gcloud builds submit --tag "$IMAGE" .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE" \
    --region "$REGION" \
    --platform managed \
    --allow-unauthenticated

# Get the service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format='value(status.url)')

echo "✅ Deployment complete!"
echo "🌐 Service URL: $SERVICE_URL"
echo "📝 Test with: curl -X POST \"$SERVICE_URL/solve\" -H \"Content-Type: application/json\" -d '{\"bot\": \"seomi\", \"task\": \"python result = 2 + 2\"}'"
echo ""
echo "🔗 For Firebase Functions, update the Cloud Run URL:"
echo "   export CLOUD_RUN_URL=\"$SERVICE_URL\""
echo "   ./deploy-firebase.sh"