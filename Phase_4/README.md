Phase 4 Student model training and evaluation

1. Install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r Phase_4/requirements.txt

2. Convert pseudo and human annotations to COCO:
   python Phase_4/scripts/convert_pseudo_to_coco.py \
     --human-dir ./Phase_1/Annotations \
     --pseudo-dir ./Phase_3/pseudo \
     --images-dir ./Phase_1/Images/BBBC005_v1_images \
     --out-dir ./Phase_4/coco

3. Train student model:
   python Phase_4/scripts/train_student.py --coco-dir ./Phase_4/coco --config Phase_4/configs/student_config.yaml

4. Evaluate student model:
   python Phase_4/scripts/evaluate_student.py \
     --images-dir ./Phase_1/Images/BBBC005_v1_images \
     --annotations-dir ./Phase_1/Annotations \
     --model-checkpoint ./Phase_4/output/model_final.pth \
     --output-dir ./Phase_4/eval
