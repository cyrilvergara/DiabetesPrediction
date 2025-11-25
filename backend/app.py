from flask import Flask, request, jsonify
import os
from model import load_model, predict as model_predict

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

    try:
        pred = model_predict(MODEL, features)
    except Exception as e:
        return jsonify({"error": f"prediction failed: {e}"}), 500

    return jsonify({"prediction": int(pred)})


if __name__ == "__main__":
    # When running locally: PORT env var will be used if set by hosting providers
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
