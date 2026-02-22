"""
Streamlit annotation app using streamlit-drawable-canvas (stable combo).
- Draw circles/ellipses on images
- Choose label before drawing (applies to new shapes)
- Compute mean intensity inside each shape (grayscale)
- Save per-image JSON to Annotations/
- Next / Previous navigation
"""

from pathlib import Path
import json
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# -------------------- PATHS (robust) --------------------
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "Images" / "BBBC005_v1_images"
ANNOT_DIR = BASE_DIR / "Annotations"
ANNOT_DIR.mkdir(exist_ok=True)

# -------------------- CONFIG --------------------
LABEL_OPTIONS = ["Empty", "Loaded", "Multilamellar", "Ruptured"]
EXTS = {".tif", ".tiff", ".png", ".jpg", ".jpeg"}

st.set_page_config(page_title="Liposome Annotation", layout="wide")

# -------------------- HELPERS --------------------

def list_images():
    if not IMAGE_DIR.exists():
        return []
    return sorted([p for p in IMAGE_DIR.iterdir() if p.suffix.lower() in EXTS])

def load_image(path: Path):
    # PIL handles TIFF; convert to RGB for display
    img = Image.open(path)
    return img.convert("RGB")

def compute_mean_intensity(pil_img, mask_bool):
    gray = np.array(pil_img.convert("L"))
    mask = mask_bool.astype(bool)
    if mask.sum() == 0:
        return None
    return float(gray[mask].mean())

def save_annotation_file(image_path: Path, payload: dict):
    out = ANNOT_DIR / f"{image_path.stem}.json"
    with open(out, "w") as f:
        json.dump(payload, f, indent=2)

def load_annotation_file(image_path: Path):
    p = ANNOT_DIR / f"{image_path.stem}.json"
    if p.exists():
        with open(p, "r") as f:
            return json.load(f)
    return None

# -------------------- UI --------------------

st.title("Cryo-TEM Liposome Annotation (Streamlit Canvas)")

image_files = list_images()
if not image_files:
    st.error(f"No images found in {IMAGE_DIR}. Put .tif images there and refresh.")
    st.stop()

# Sidebar navigation
st.sidebar.header("Navigation")
idx = st.sidebar.number_input(
    "Image index",
    min_value=0,
    max_value=len(image_files) - 1,
    value=0,
    step=1
)
current_path = image_files[idx]
st.sidebar.write(f"File: `{current_path.name}`")

# Annotation settings
st.sidebar.header("Annotation settings")
current_label = st.sidebar.selectbox("Label for new shapes", LABEL_OPTIONS, index=1)
drawing_mode = st.sidebar.selectbox("Drawing mode", ["circle", "rect", "freedraw"], index=0)
stroke_width = st.sidebar.slider("Stroke width", 1, 10, 3)
stroke_color = st.sidebar.color_picker("Stroke color", "#FF0000")

# Load image
pil_img = load_image(current_path)
w, h = pil_img.size

# Load existing annotations (if any) to show JSON on the side
existing = load_annotation_file(current_path)

# Canvas
st.markdown("### Draw shapes on the image (choose label first)")
canvas_result = st_canvas(
    fill_color="rgba(0,0,0,0)",  # transparent fill
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_image=pil_img,
    update_streamlit=True,
    height=h,
    width=w,
    drawing_mode=drawing_mode,
    key=f"canvas_{current_path.name}",
)

# Process objects returned by canvas
objects = canvas_result.json_data.get("objects", []) if canvas_result.json_data else []
annotations = []

for i, obj in enumerate(objects):
    # We handle circle (fabric circle) and ellipse-like objects (fabric ellipse)
    obj_type = obj.get("type", "")
    # For circle/ellipse, canvas returns left, top, radiusX/radiusY or radius
    if obj_type in ("circle", "ellipse", "rect", "path", "polygon"):
        # For circle: radius property exists
        if obj_type == "circle":
            left = obj.get("left", 0)
            top = obj.get("top", 0)
            radius = obj.get("radius", obj.get("radiusX", 0))
            center_x = left + radius
            center_y = top + radius
            rx = ry = radius
        elif obj_type == "ellipse":
            left = obj.get("left", 0)
            top = obj.get("top", 0)
            rx = obj.get("rx", obj.get("radiusX", 0))
            ry = obj.get("ry", obj.get("radiusY", 0))
            center_x = left + rx
            center_y = top + ry
        elif obj_type == "rect":
            left = obj.get("left", 0)
            top = obj.get("top", 0)
            width = obj.get("width", 0) * obj.get("scaleX", 1)
            height = obj.get("height", 0) * obj.get("scaleY", 1)
            center_x = left + width / 2
            center_y = top + height / 2
            rx = width / 2
            ry = height / 2
        else:
            # fallback: skip complex shapes
            continue

        # Build boolean mask for ellipse/circle area
        yy, xx = np.ogrid[:h, :w]
        mask = ((xx - center_x) ** 2) / (rx ** 2 + 1e-8) + ((yy - center_y) ** 2) / (ry ** 2 + 1e-8) <= 1

        mean_intensity = compute_mean_intensity(pil_img, mask)

        annotations.append({
            "id": i,
            "type": obj_type,
            "label": current_label,
            "center_x": float(center_x),
            "center_y": float(center_y),
            "radius_x": float(rx),
            "radius_y": float(ry),
            "mean_intensity": mean_intensity
        })

# Show annotation summary
st.markdown("### Current annotations (preview)")
st.write(f"Detected shapes on canvas: **{len(annotations)}**")
st.json(annotations)

# Save button
if st.button("Save annotations for this image"):
    payload = {
        "image_id": current_path.name,
        "width": w,
        "height": h,
        "num_annotations": len(annotations),
        "annotations": annotations
    }
    save_annotation_file(current_path, payload)
    st.success(f"Saved {current_path.stem}.json to Annotations/")

# Show existing saved annotations if present
if existing:
    st.markdown("### Existing saved annotations (file)")
    st.json(existing)

# Quick navigation buttons
col1, col2 = st.columns(2)
if col1.button("Previous image"):
    new_idx = max(0, idx - 1)
    st.experimental_rerun()  # user can change index in sidebar; rerun will pick new value
if col2.button("Next image"):
    new_idx = min(len(image_files) - 1, idx + 1)
    st.experimental_rerun()
