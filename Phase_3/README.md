Phase 3 — Teacher model and pseudo-label generation

1. Install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r Phase_3/requirements.txt

2. Convert Phase_1 annotations to COCO:
   python Phase_3/scripts/convert_phase1_to_coco.py \
     --annotations-dir ./Phase_1/Annotations \
     --images-dir ./Phase_1/Images/BBBC005_v1_images \
     --out-dir ./Phase_3/coco

3. Train teacher (Detectron2):
   python Phase_3/scripts/train_teacher.py --coco-dir ./Phase_3/coco --config Phase_3/configs/teacher_config.yaml

4. Generate pseudo-labels:
   python Phase_3/scripts/generate_pseudo_labels.py \
     --images-dir ./Phase_1/Images/BBBC005_v1_images \
     --output-dir ./Phase_3/pseudo \
     --model-checkpoint ./Phase_3/output/model_final.pth \
     --confidence 0.9
