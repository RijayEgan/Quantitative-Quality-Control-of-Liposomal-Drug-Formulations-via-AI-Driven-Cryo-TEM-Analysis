#!/usr/bin/env python3
"""
Validate annotation JSON files against schema and perform image-aware checks.
Usage:
  python validate_annotations.py --annotations-dir ./Annotations --images-dir ./Images --schema schema/annotation_schema.json --fix
"""

import argparse
import json
import shutil
from pathlib import Path
from typing import Tuple, List
import sys

import jsonschema
from PIL import Image
import numpy as np

def load_schema(path: Path):
    with open(path, "r") as f:
        return json.load(f)

def validate_schema(data: dict, schema: dict) -> Tuple[bool, List[str]]:
    validator = jsonschema.Draft7Validator(schema)
    errors = []
    for err in validator.iter_errors(data):
        errors.append(f"{err.message} at {'/'.join(map(str, err.path))}")
    return (len(errors) == 0, errors)

def load_image_size(images_dir: Path, image_id: str) -> Tuple[int,int]:
    p = images_dir / image_id
    if not p.exists():
        raise FileNotFoundError(f"Image file not found: {p}")
    with Image.open(p) as im:
        return im.size

def semantic_checks(data: dict, img_size: Tuple[int,int]) -> List[str]:
    w, h = img_size
    errs = []
    if data.get("width") != w or data.get("height") != h:
        errs.append(f"Declared image size ({data.get('width')},{data.get('height')}) "
                    f"does not match actual ({w},{h})")
    annos = data.get("annotations", [])
    if len(annos) != data.get("num_annotations", len(annos)):
        errs.append(f"num_annotations {data.get('num_annotations')} != actual {len(annos)}")
    for a in annos:
        cx = a.get("center_x")
        cy = a.get("center_y")
        rx = a.get("radius_x")
        ry = a.get("radius_y")
        if not isinstance(cx, (int, float)) or not isinstance(cy, (int, float)):
            errs.append(f"Annotation id {a.get('id')}: center coordinates must be numeric")
            continue
        if not (0 <= cx <= w) or not (0 <= cy <= h):
            errs.append(f"Annotation id {a.get('id')}: center ({cx},{cy}) outside image bounds")
        if not (isinstance(rx, (int, float)) and isinstance(ry, (int, float))):
            errs.append(f"Annotation id {a.get('id')}: radii must be numeric")
            continue
        if rx <= 0 or ry <= 0:
            errs.append(f"Annotation id {a.get('id')}: radii must be positive")
        # optional: check that ellipse fits inside image bounds
        if (cx - rx) < 0 or (cx + rx) > w or (cy - ry) < 0 or (cy + ry) > h:
            errs.append(f"Annotation id {a.get('id')}: ellipse extends outside image bounds")
        mi = a.get("mean_intensity")
        if mi is not None and not isinstance(mi, (int, float)):
            errs.append(f"Annotation id {a.get('id')}: mean_intensity must be number or null")
    return errs

def validate_file(path: Path, schema: dict, images_dir: Path) -> Tuple[bool, List[str]]:
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Failed to parse JSON: {e}"]
    ok_schema, schema_errs = validate_schema(data, schema)
    if not ok_schema:
        return False, schema_errs
    try:
        img_size = load_image_size(images_dir, data["image_id"])
    except Exception as e:
        return False, [str(e)]
    sem_errs = semantic_checks(data, img_size)
    if sem_errs:
        return False, sem_errs
    return True, []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations-dir", required=True, type=Path)
    parser.add_argument("--images-dir", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--fix", action="store_true", help="Move valid files to validated/ and invalid to errors/")
    args = parser.parse_args()

    schema = load_schema(args.schema)
    ann_dir = args.annotations_dir
    img_dir = args.images_dir

    validated_dir = ann_dir / "validated"
    errors_dir = ann_dir / "errors"
    if args.fix:
        validated_dir.mkdir(exist_ok=True)
        errors_dir.mkdir(exist_ok=True)

    json_files = sorted([p for p in ann_dir.glob("*.json") if p.is_file()])
    if not json_files:
        print("No JSON files found in", ann_dir)
        sys.exit(0)

    summary = {"total": 0, "valid": 0, "invalid": 0}
    for jf in json_files:
        summary["total"] += 1
        ok, errs = validate_file(jf, schema, img_dir)
        if ok:
            summary["valid"] += 1
            print(f"[OK] {jf.name}")
            if args.fix:
                shutil.move(str(jf), str(validated_dir / jf.name))
        else:
            summary["invalid"] += 1
            print(f"[ERR] {jf.name}")
            for e in errs:
                print("   -", e)
            if args.fix:
                shutil.move(str(jf), str(errors_dir / jf.name))

    print("Validation complete. Total:", summary["total"], "Valid:", summary["valid"], "Invalid:", summary["invalid"])

if __name__ == "__main__":
    main()
