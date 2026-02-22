# Phase 5: Deployment and packaging

This directory contains a minimal scaffold for deploying the inference API.

- scripts/app.py — Flask API placeholder with /health and /predict.
- scripts/package_model.py — simple model packaging helper.
- deploy/Dockerfile — container image for the API.
- deploy/deploy.sh — helper to build and run the container.
- tests/ — pytest smoke test for the API.
