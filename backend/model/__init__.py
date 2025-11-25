"""Model loading and prediction for Diabetes Prediction.

This module loads the trained TensorFlow/Keras ANN model and provides
prediction functionality with proper feature preprocessing.
"""

import os
import numpy as np
import tensorflow as tf
import pickle

# Define feature order (must match training data)
FEATURE_ORDER = [
    "pregnancies",
    "glucose",
    "blood_pressure",
    "skin_thickness",
    "insulin",
    "bmi",
    "diabetes_pedigree_function",
    "age"
]

MODEL_DIR = os.path.join(os.path.dirname(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "model.h5")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

# Global variables to cache loaded model and scaler
_model = None
_scaler = None


def load_model():
    """Load the trained TensorFlow/Keras model and scaler.
    
    Returns:
        tuple: (model, scaler) - The loaded model and scaler objects
    """
    global _model, _scaler
    
    if _model is None or _scaler is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Please run train_model.py first to train and save the model."
            )
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(
                f"Scaler file not found at {SCALER_PATH}. "
                "Please run train_model.py first to train and save the scaler."
            )
        
        # Load model
        _model = tf.keras.models.load_model(MODEL_PATH)
        
        # Load scaler
        with open(SCALER_PATH, 'rb') as f:
            _scaler = pickle.load(f)
    
    return _model, _scaler


def predict(model_data, features):
    """Make a prediction using the trained model.
    
    Args:
        model_data: Tuple of (model, scaler) from load_model()
        features: Dict with feature names as keys, or list/array in feature order
        
    Returns:
        tuple: (prediction, probability) - Binary prediction (0 or 1) and probability score
    """
    model, scaler = model_data
    
    # Convert features dict to numpy array in correct order
    if isinstance(features, dict):
        feature_array = np.array([[features.get(feat, 0) for feat in FEATURE_ORDER]], dtype=np.float32)
    elif isinstance(features, (list, tuple, np.ndarray)):
        # Assume features are already in correct order
        feature_array = np.array([features], dtype=np.float32)
        if feature_array.shape[1] != len(FEATURE_ORDER):
            raise ValueError(
                f"Expected {len(FEATURE_ORDER)} features, got {feature_array.shape[1]}"
            )
    else:
        raise TypeError("Features must be a dict, list, tuple, or numpy array")
    
    # Normalize features using the scaler
    feature_array_scaled = scaler.transform(feature_array)
    
    # Make prediction
    probability = model.predict(feature_array_scaled, verbose=0)[0][0]
    prediction = 1 if probability > 0.5 else 0
    
    return prediction, float(probability)
