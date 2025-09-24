#!/bin/bash

# Build script for CloudHSM Management Dashboard

set -e

IMAGE_NAME="cloudhsm-dashboard"
TAG="${1:-latest}"

echo "Building CloudHSM Management Dashboard Docker image..."
echo "Image: ${IMAGE_NAME}:${TAG}"

# Build the Docker image
docker build -f Dockerfile -t "${IMAGE_NAME}:${TAG}" .

echo "Build completed successfully!"
echo "To run the container:"
echo "  docker run -p 8000:8000 --privileged ${IMAGE_NAME}:${TAG}"
echo ""
echo "Or use docker-compose:"
echo "  APP_PORT=8000 docker-compose up"