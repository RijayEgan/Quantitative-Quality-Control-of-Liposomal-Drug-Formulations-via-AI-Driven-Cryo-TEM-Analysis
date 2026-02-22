import io
from PIL import Image
from Phase_5.scripts import app as app_module
import pytest

def test_health_endpoint():
    client = app_module.app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json.get("status") == "ok"

def test_predict_no_image():
    client = app_module.app.test_client()
    r = client.post("/predict")
    assert r.status_code == 400
