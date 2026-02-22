#!/usr/bin/env python3
"""
Convert Phase_1 JSON annotations (per-image) into COCO-style train/val JSONs.
Usage:
  python convert_phase1_to_coco.py --annotations-dir ../Phase_1/Annotations --images-dir ../Phase_1/Images/BBBC005_v1_images --out-dir ./Phase_3/coco
"""
import argparse
import json
from pathlib import Path
from utils.coco_utils import build_coco_template, save_coco_json

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--annotations-dir", required=True, type=Path)
    p.add_argument("--images-dir", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    p.add_argument("--val-split", type=float, default=0.1)
    return p.parse_args()

def main():
    args = parse_args()
    ann_dir = args.annotations_dir
    img_dir = args.images_dir
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted([p for p in ann_dir.glob("*.json")])
    images = []
    annotations = []
    ann_id = 1
    img_id = 1
    for jf in files:
        data = json.load(open(jf))
        image_name = data["image_id"]
        img_path = img_dir / image_name
        if not img_path.exists():
            print("Skipping, image not found:", image_name)
            continue
        width = data.get("width")
        height = data.get("height")
        images.append({
            "id": img_id,
            "file_name": str(img_path.resolve()),
            "width": width,
            "height": height
        })
        for a in data.get("annotations", []):
            cx = a["center_x"]
            cy = a["center_y"]
            rx = a["radius_x"]
            ry = a["radius_y"]
            x = cx - rx
            y = cy - ry
            w = rx * 2
            h = ry * 2
            annotations.append({
                "id": ann_id,
                "image_id": img_id,
                "category_id": 1,
                "bbox": [x, y, w, h],
                "area": w * h,
                "iscrowd": 0,
                "segmentation": []
            })
            ann_id += 1
        img_id += 1

    n = len(images)
    n_val = max(1, int(n * args.val_split))
    val_images = images[:n_val]
    train_images = images[n_val:]

    def build_coco(images_list):
        coco = build_coco_template()
        coco["images"] = images_list
        image_ids = {im["id"] for im in images_list}
        coco["annotations"] = [a for a in annotations if a["image_id"] in image_ids]
        return coco

    save_coco_json(build_coco(train_images), out_dir / "train.json")
    save_coco_json(build_coco(val_images), out_dir / "val.json")
    print("Wrote COCO train/val to", out_dir)

if __name__ == "__main__":
    main()
