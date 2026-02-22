from Phase_5.scripts import app as app_module

def test_health():
    client = app_module.app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json.get("status") == "ok"
