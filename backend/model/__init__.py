"""Simple model stub for initial backend skeleton.

This file exposes two helpers:
- load_model(): returns a lightweight placeholder model object
- predict(model, features): returns a deterministic dummy prediction

Replace these with your trained model loading and inference logic later.
"""

def load_model():
    # Placeholder: in future this will load a saved ML model (e.g., TensorFlow/Keras/Joblib)
    return {"type": "stub"}


def predict(model, features):
    """Basic deterministic rule for demo and tests.

    Accepts either a dict of named features or an ordered list.
    A tiny rule: if glucose > 125 => positive (1), else negative (0).
    This keeps the endpoint functional while the real model is integrated.
    """
    glucose = None
    if isinstance(features, dict):
        glucose = features.get("glucose")
    elif isinstance(features, (list, tuple)) and len(features) > 0:
        # assume glucose is the second column in some datasets, fallback to index 1
        try:
            glucose = features[1]
        except Exception:
            glucose = None

    try:
        if glucose is None:
            return 0
        g = float(glucose)
        return 1 if g > 125 else 0
    except Exception:
        return 0
