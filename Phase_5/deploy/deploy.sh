#!/usr/bin/env bash
set -euo pipefail
IMAGE_NAME="${1:-liposome-student:latest}"
docker build -t "$IMAGE_NAME" -f Phase_5/deploy/Dockerfile .
echo "Built $IMAGE_NAME"
# run container (detached)
docker run -d -p 8000:8000 --name liposome_api "$IMAGE_NAME"
