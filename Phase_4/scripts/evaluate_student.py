#!/usr/bin/env python3
"""
Run student inference on a set of images and compute simple aggregate metrics.
Usage:
  python evaluate_student.py --images-dir ../Phase_1/Images/BBBC005_v1_images --annotations-dir ../Phase_1/Annotations --model-checkpoint ./Phase_4/output/model_final.pth --output-dir ./Phase_4/eval
"""
import argparse
from pathlib import Path
import json
from PIL import Image
import numpy as np
from tqdm import tqdm
import datetime
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
import yaml
from utils.metrics import compute_detection_metrics

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--images-dir", required=True, type=Path)
    p.add_argument("--annotations-dir", required=True, type=Path)
    p.add_argument("--model-checkpoint", required=True, type=Path)
    p.add_argument("--config", type=Path, default=Path("Phase_4/configs/student_config.yaml"))
    p.add_argument("--output-dir", required=True, type=Path)
    return p.parse_args()

def load_cfg(config_path, checkpoint_path):
    with open(config_path, "r") as f:
        cfg_dict = yaml.safe_load(f)
    cfg = get_cfg()
    cfg.merge_from_file("detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.WEIGHTS = str(checkpoint_path)
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.DEVICE = "cuda" if detectron2.utils.env.get_cuda_device_count() > 0 else "cpu"
    return cfg

def mask_count_from_annotation(json_path):
    data = json.load(open(json_path))
    return data.get("num_annotations", 0)

def main():
    args = parse_args()
    cfg = load_cfg(args.config, args.model_checkpoint)
    predictor = DefaultPredictor(cfg)
    images = sorted([p for p in args.images_dir.iterdir() if p.suffix.lower() in [".tif",".tiff",".png",".jpg",".jpeg"]])
    y_true_counts = []
    y_pred_counts = []
    for img_path in tqdm(images):
        ann_path = args.annotations_dir / f"{img_path.stem}.json"
        true_count = mask_count_from_annotation(ann_path) if ann_path.exists() else 0
        y_true_counts.append(true_count)
        pil = Image.open(img_path).convert("RGB")
        im = np.array(pil)[:, :, ::-1]
        outputs = predictor(im)
        instances = outputs["instances"].to("cpu")
        pred_count = len(instances)
        y_pred_counts.append(pred_count)
    metrics = compute_detection_metrics(y_true_counts, y_pred_counts)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with open(args.output_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("Evaluation complete. Metrics:", metrics)

if __name__ == "__main__":
    main()
