import json
from pathlib import Path
from typing import Dict

def save_coco_json(data: Dict, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

def build_coco_template():
    return {
        "info": {"description": "Liposome dataset"},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, "name": "liposome"}]
    }
