import json

from app import app


def test_index():
    client = app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "ok"


def test_predict_stub():
    client = app.test_client()
    rv = client.post("/predict", json={"features": {"glucose": 130}})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["prediction"] == 1
