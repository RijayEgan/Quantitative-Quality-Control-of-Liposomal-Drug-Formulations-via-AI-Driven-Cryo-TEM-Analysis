#!/usr/bin/env python3
"""
Convert Phase_3 pseudo JSONs and Phase_1 human JSONs into COCO-style train/val for student training.
Usage:
  python convert_pseudo_to_coco.py --human-dir ../Phase_1/Annotations --pseudo-dir ../Phase_3/pseudo --images-dir ../Phase_1/Images/BBBC005_v1_images --out-dir ./Phase_4/coco --val-split 0.1 --pseudo-weight 0.5
"""
import argparse
import json
from pathlib import Path
from math import ceil
from collections import defaultdict

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--human-dir", required=True, type=Path)
    p.add_argument("--pseudo-dir", required=True, type=Path)
    p.add_argument("--images-dir", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    p.add_argument("--val-split", type=float, default=0.1)
    p.add_argument("--pseudo-weight", type=float, default=0.5)
    return p.parse_args()

def build_coco_entries(json_paths, img_dir, start_img_id=1, start_ann_id=1, source="human"):
    images = []
    annotations = []
    img_id = start_img_id
    ann_id = start_ann_id
    for jf in sorted(json_paths):
        data = json.load(open(jf))
        image_name = data["image_id"]
        img_path = img_dir / image_name
        if not img_path.exists():
            continue
        width = data.get("width")
        height = data.get("height")
        images.append({"id": img_id, "file_name": str(img_path.resolve()), "width": width, "height": height, "source": source})
        for a in data.get("annotations", []):
            cx = a["center_x"]
            cy = a["center_y"]
            rx = a["radius_x"]
            ry = a["radius_y"]
            x = cx - rx
            y = cy - ry
            w = rx * 2
            h = ry * 2
            annotations.append({"id": ann_id, "image_id": img_id, "category_id": 1, "bbox": [x, y, w, h], "area": w*h, "iscrowd": 0})
            ann_id += 1
        img_id += 1
    return images, annotations, img_id, ann_id

def save_coco(coco, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(coco, f, indent=2)

def main():
    args = parse_args()
    human_files = sorted([p for p in args.human_dir.glob("*.json")])
    pseudo_files = sorted([p for p in args.pseudo_dir.glob("*.json")])
    images_h, ann_h, next_img_id, next_ann_id = build_coco_entries(human_files, args.images_dir, 1, 1, "human")
    images_p, ann_p, _, _ = build_coco_entries(pseudo_files, args.images_dir, next_img_id, next_ann_id, "pseudo")
    all_images = images_h + images_p
    all_annotations = ann_h + ann_p
    # simple split by images
    n = len(all_images)
    n_val = max(1, int(n * args.val_split))
    val_images = all_images[:n_val]
    train_images = all_images[n_val:]
    image_id_set_val = {im["id"] for im in val_images}
    coco_template = {"info": {"description": "Liposome student dataset"}, "licenses": [], "images": [], "annotations": [], "categories": [{"id":1,"name":"liposome"}]}
    coco_train = coco_template.copy()
    coco_train["images"] = train_images
    coco_train["annotations"] = [a for a in all_annotations if a["image_id"] in {im["id"] for im in train_images}]
    coco_val = coco_template.copy()
    coco_val["images"] = val_images
    coco_val["annotations"] = [a for a in all_annotations if a["image_id"] in image_id_set_val]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    save_coco(coco_train, args.out_dir / "train.json")
    save_coco(coco_val, args.out_dir / "val.json")
    print("Wrote COCO train/val to", args.out_dir)

if __name__ == "__main__":
    main()
