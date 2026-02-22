#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${1:-phase5-api:latest}"
CONTAINER_NAME="${2:-phase5_api}"

docker build -t "$IMAGE_NAME" -f Phase_5/deploy/Dockerfile .
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  docker rm -f "$CONTAINER_NAME"
fi
docker run -d -p 8000:8000 --name "$CONTAINER_NAME" "$IMAGE_NAME"
echo "Deployed $IMAGE_NAME as $CONTAINER_NAME"
