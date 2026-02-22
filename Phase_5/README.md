Phase 5 Deployment and Packaging

Contents:
- scripts/app.py: Flask inference API (placeholder)
- scripts/package_model.py: export/packaging helper (placeholder)
- deploy/Dockerfile and deploy/deploy.sh: container build and run
- ci workflow: .github/workflows/phase5-ci.yml runs tests on push
- tests: basic pytest smoke tests

Usage:
1. Build package (placeholder):
   python Phase_5/scripts/package_model.py --checkpoint ./Phase_4/output/model_final.pth --out ./Phase_5/package/model.onnx

2. Run API locally:
   python Phase_5/scripts/app.py --model ./Phase_4/output/model_final.pth --port 8000

3. Build and run Docker:
   Phase_5/deploy/deploy.sh my-image:latest
