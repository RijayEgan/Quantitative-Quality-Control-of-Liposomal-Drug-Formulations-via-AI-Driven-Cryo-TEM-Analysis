#!/usr/bin/env python3
"""
Lightweight inference API for the student model.
Usage:
  python app.py --model ./Phase_4/output/model_final.pth --port 8000
"""
import argparse
import json
from pathlib import Path
from PIL import Image
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)
MODEL = None

def load_model(path):
    # placeholder: load your PyTorch/Detectron2 model here
    return {"model_path": str(path)}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"})

@app.route("/predict", methods=["POST"])
def predict():
    if MODEL is None:
        return jsonify({"error":"model not loaded"}), 500
    data = request.files.get("image")
    if data is None:
        return jsonify({"error":"no image provided"}), 400
    img = Image.open(data.stream).convert("RGB")
    w, h = img.size
    # placeholder response
    return jsonify({"image_size":[w,h], "predictions": []})

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True, type=Path)
    p.add_argument("--port", type=int, default=8000)
    return p.parse_args()

def main():
    global MODEL
    args = parse_args()
    MODEL = load_model(args.model)
    app.run(host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()
