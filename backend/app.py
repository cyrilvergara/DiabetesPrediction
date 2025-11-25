from flask import Flask, request, jsonify
import os
from model import load_model, predict as model_predict, FEATURE_ORDER

app = Flask(__name__, static_folder="../client/dist", static_url_path="/")
MODEL = load_model()


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/<path:path>")
def static_proxy(path):
    # serve static files if they exist, otherwise fallback to index.html
    if os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    return app.send_static_file("index.html")


@app.route("/predict", methods=["POST"])
def predict_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid or missing JSON body"}), 400

    features = data.get("features")
    if features is None:
        return jsonify({"error": "missing 'features' in request body"}), 400

    # Validate features dict
    if not isinstance(features, dict):
        return jsonify({"error": "features must be a dictionary"}), 400

    # Check for all required features
    missing_features = [feat for feat in FEATURE_ORDER if feat not in features]
    if missing_features:
        return jsonify({
            "error": f"missing required features: {', '.join(missing_features)}"
        }), 400

    # Validate feature types and ranges
    validation_errors = []
    feature_ranges = {
        "pregnancies": (0, 20),
        "glucose": (0, 500),
        "blood_pressure": (0, 200),
        "skin_thickness": (0, 100),
        "insulin": (0, 1000),
        "bmi": (0, 100),
        "diabetes_pedigree_function": (0, 5),
        "age": (0, 150)
    }

    for feat in FEATURE_ORDER:
        value = features.get(feat)
        try:
            value_float = float(value)
            min_val, max_val = feature_ranges[feat]
            if value_float < min_val or value_float > max_val:
                validation_errors.append(
                    f"{feat} must be between {min_val} and {max_val}, got {value_float}"
                )
        except (ValueError, TypeError):
            validation_errors.append(f"{feat} must be a valid number, got {type(value).__name__}")

    if validation_errors:
        return jsonify({
            "error": "validation failed",
            "details": validation_errors
        }), 400

    try:
        prediction, probability = model_predict(MODEL, features)
        return jsonify({
            "prediction": int(prediction),
            "probability": round(probability, 4),
            "confidence": round(abs(probability - 0.5) * 2, 4)  # Convert to 0-1 scale
        })
    except Exception as e:
        return jsonify({"error": f"prediction failed: {str(e)}"}), 500


if __name__ == "__main__":
    # When running locally: PORT env var will be used if set by hosting providers
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
