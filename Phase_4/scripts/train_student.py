#!/usr/bin/env python3
"""
Train a Detectron2 student model using COCO train/val produced by convert_pseudo_to_coco.py
Usage:
  python train_student.py --coco-dir ./Phase_4/coco --config Phase_4/configs/student_config.yaml
"""
import argparse
from pathlib import Path
import yaml
import os

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--coco-dir", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    return p.parse_args()

def main():
    args = parse_args()
    from detectron2.engine import DefaultTrainer
    from detectron2.config import get_cfg
    from detectron2.data.datasets import register_coco_instances

    train_json = str(args.coco_dir / "train.json")
    val_json = str(args.coco_dir / "val.json")

    register_coco_instances("liposome_student_train", {}, train_json, "")
    register_coco_instances("liposome_student_val", {}, val_json, "")

    with open(args.config, "r") as f:
        cfg_dict = yaml.safe_load(f)

    cfg = get_cfg()
    cfg.merge_from_file("detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.WEIGHTS = cfg_dict["MODEL"]["WEIGHTS"]
    cfg.MODEL.MASK_ON = cfg_dict["MODEL"]["MASK_ON"]
    cfg.SOLVER.IMS_PER_BATCH = cfg_dict["SOLVER"]["IMS_PER_BATCH"]
    cfg.SOLVER.BASE_LR = cfg_dict["SOLVER"]["BASE_LR"]
    cfg.SOLVER.MAX_ITER = cfg_dict["SOLVER"]["MAX_ITER"]
    cfg.SOLVER.STEPS = cfg_dict["SOLVER"]["STEPS"]
    cfg.INPUT.MIN_SIZE_TRAIN = tuple(cfg_dict["INPUT"]["MIN_SIZE_TRAIN"])
    cfg.INPUT.MAX_SIZE_TRAIN = cfg_dict["INPUT"]["MAX_SIZE_TRAIN"]
    cfg.OUTPUT_DIR = cfg_dict.get("OUTPUT_DIR", "./Phase_4/output")
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()

if __name__ == "__main__":
    main()
