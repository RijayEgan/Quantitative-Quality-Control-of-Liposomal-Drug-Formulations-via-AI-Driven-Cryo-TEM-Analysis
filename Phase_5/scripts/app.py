#!/usr/bin/env python3
from flask import Flask, request, jsonify
from pathlib import Path
from PIL import Image

app = Flask(__name__)
MODEL = None

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    if MODEL is None:
        return jsonify({"error": "model not loaded"}), 500
    f = request.files.get("image")
    if not f:
        return jsonify({"error": "no image provided"}), 400
    try:
        img = Image.open(f.stream).convert("RGB")
    except Exception as exc:
        return jsonify({"error": f"failed to read image: {exc}"}), 400
    w, h = img.size
    return jsonify({"image_size": [w, h], "predictions": []})

def load_model(path: Path | None):
    if path is None:
        return None
    return {"model_path": str(path)}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=False, type=Path, help="Path to model file")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    MODEL = load_model(args.model) if args.model else None
    app.run(host="0.0.0.0", port=args.port)
