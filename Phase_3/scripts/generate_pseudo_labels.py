#!/usr/bin/env python3
"""
Run teacher inference and write pseudo-labels in Phase_2 schema format.
Usage:
  python generate_pseudo_labels.py --images-dir ../Phase_1/Images/BBBC005_v1_images --output-dir ./Phase_3/pseudo --model-checkpoint ./Phase_3/output/model_final.pth --confidence 0.9
"""
import argparse
from pathlib import Path
import json
import numpy as np
from PIL import Image
from tqdm import tqdm
import datetime

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--images-dir", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--model-checkpoint", required=True, type=Path)
    p.add_argument("--confidence", type=float, default=0.9)
    p.add_argument("--config", type=Path, default=Path("Phase_3/configs/teacher_config.yaml"))
    return p.parse_args()

def load_cfg(config_path, checkpoint_path):
    import yaml
    from detectron2.config import get_cfg
    import detectron2
    with open(config_path, "r") as f:
        cfg_dict = yaml.safe_load(f)
    cfg = get_cfg()
    cfg.merge_from_file("detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.WEIGHTS = str(checkpoint_path)
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.0
    cfg.MODEL.DEVICE = "cuda" if detectron2.utils.env.get_cuda_device_count() > 0 else "cpu"
    cfg.INPUT.MIN_SIZE_TEST = cfg_dict["INPUT"]["MIN_SIZE_TEST"]
    cfg.INPUT.MAX_SIZE_TEST = cfg_dict["INPUT"]["MAX_SIZE_TEST"]
    return cfg

def mask_to_ellipse(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    cx = float(xs.mean())
    cy = float(ys.mean())
    cov = np.cov(xs, ys)
    eigvals, eigvecs = np.linalg.eig(cov)
    rx = float(np.sqrt(abs(eigvals[0])) * 2.5)
    ry = float(np.sqrt(abs(eigvals[1])) * 2.5)
    return cx, cy, abs(rx), abs(ry)

def compute_mean_intensity(pil_img, mask):
    gray = np.array(pil_img.convert("L"))
    if mask.sum() == 0:
        return None
    return float(gray[mask].mean())

def main():
    args = parse_args()
    images = sorted([p for p in args.images_dir.iterdir() if p.suffix.lower() in [".tif",".tiff",".png",".jpg",".jpeg"]])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cfg = load_cfg(args.config, args.model_checkpoint)

    from detectron2.engine import DefaultPredictor
    predictor = DefaultPredictor(cfg)

    manifest = []
    for img_path in tqdm(images):
        pil = Image.open(img_path).convert("RGB")
        im = np.array(pil)[:, :, ::-1]
        outputs = predictor(im)
        instances = outputs["instances"].to("cpu")
        scores = instances.scores.numpy()
        masks = instances.pred_masks.numpy() if instances.has("pred_masks") else None
        selected = np.where(scores >= args.confidence)[0]
        annotations = []
        for i in selected:
            score = float(scores[i])
            mask = masks[i] if masks is not None else None
            if mask is None:
                continue
            ellipse = mask_to_ellipse(mask)
            if ellipse is None:
                continue
            cx, cy, rx, ry = ellipse
            mean_int = compute_mean_intensity(pil, mask)
            annotations.append({
                "id": len(annotations),
                "type": "ellipse",
                "label": "pseudo",
                "center_x": float(cx),
                "center_y": float(cy),
                "radius_x": float(rx),
                "radius_y": float(ry),
                "mean_intensity": mean_int,
                "confidence": score
            })
        out = {
            "image_id": img_path.name,
            "width": pil.width,
            "height": pil.height,
            "num_annotations": len(annotations),
            "annotations": annotations,
            "provenance": {
                "model_checkpoint": str(args.model_checkpoint),
                "confidence_threshold": args.confidence,
                "generated_at": datetime.datetime.utcnow().isoformat() + "Z"
            }
        }
        out_path = args.output_dir / f"{img_path.stem}.json"
        with open(out_path, "w") as f:
            json.dump(out, f, indent=2)
        manifest.append({"image": str(img_path.resolve()), "annotation": str(out_path.resolve()), "num": len(annotations)})
    with open(args.output_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print("Pseudo-label generation complete. Wrote to", args.output_dir)

if __name__ == "__main__":
    main()
