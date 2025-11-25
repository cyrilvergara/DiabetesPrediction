import json

from app import app


def test_index():
    """Test that the index route serves HTML."""
    client = app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    assert rv.content_type == 'text/html; charset=utf-8'


def test_predict_valid_input():
    """Test prediction with valid input containing all required features."""
    client = app.test_client()
    valid_features = {
        "pregnancies": 6,
        "glucose": 148,
        "blood_pressure": 72,
        "skin_thickness": 35,
        "insulin": 0,
        "bmi": 33.6,
        "diabetes_pedigree_function": 0.627,
        "age": 50
    }
    rv = client.post("/predict", json={"features": valid_features})
    assert rv.status_code == 200
    data = rv.get_json()
    assert "prediction" in data
    assert "probability" in data
    assert "confidence" in data
    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1
    assert 0 <= data["confidence"] <= 1


def test_predict_missing_features():
    """Test that missing features return an error."""
    client = app.test_client()
    # Missing some features
    incomplete_features = {
        "glucose": 130,
        "blood_pressure": 80
    }
    rv = client.post("/predict", json={"features": incomplete_features})
    assert rv.status_code == 400
    data = rv.get_json()
    assert "error" in data
    assert "missing required features" in data["error"].lower()


def test_predict_invalid_feature_types():
    """Test that invalid feature types return an error."""
    client = app.test_client()
    invalid_features = {
        "pregnancies": "not a number",
        "glucose": 148,
        "blood_pressure": 72,
        "skin_thickness": 35,
        "insulin": 0,
        "bmi": 33.6,
        "diabetes_pedigree_function": 0.627,
        "age": 50
    }
    rv = client.post("/predict", json={"features": invalid_features})
    assert rv.status_code == 400
    data = rv.get_json()
    assert "error" in data
    assert "validation" in data["error"].lower() or "number" in data["error"].lower()


def test_predict_out_of_range_values():
    """Test that out-of-range feature values return an error."""
    client = app.test_client()
    out_of_range_features = {
        "pregnancies": 6,
        "glucose": 1000,  # Out of range (max 500)
        "blood_pressure": 72,
        "skin_thickness": 35,
        "insulin": 0,
        "bmi": 33.6,
        "diabetes_pedigree_function": 0.627,
        "age": 50
    }
    rv = client.post("/predict", json={"features": out_of_range_features})
    assert rv.status_code == 400
    data = rv.get_json()
    assert "error" in data
    assert "validation" in data["error"].lower() or "range" in data["error"].lower()


def test_predict_missing_json_body():
    """Test that missing JSON body returns an error."""
    client = app.test_client()
    rv = client.post("/predict", data="not json")
    assert rv.status_code == 400
    data = rv.get_json()
    assert "error" in data


def test_predict_missing_features_key():
    """Test that missing 'features' key returns an error."""
    client = app.test_client()
    rv = client.post("/predict", json={})
    assert rv.status_code == 400
    data = rv.get_json()
    assert "error" in data
    assert "features" in data["error"].lower()


def test_predict_features_not_dict():
    """Test that features must be a dictionary."""
    client = app.test_client()
    rv = client.post("/predict", json={"features": [1, 2, 3]})
    assert rv.status_code == 400
    data = rv.get_json()
    assert "error" in data
    assert "dictionary" in data["error"].lower()
