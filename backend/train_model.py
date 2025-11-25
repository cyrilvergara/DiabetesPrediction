"""
Model Training Script for Diabetes Prediction
Trains an Artificial Neural Network (ANN) on the Pima Indians Diabetes Dataset.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import pickle

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Dataset URL (Pima Indians Diabetes Dataset from UCI ML Repository)
DATASET_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
DATASET_COLUMNS = [
    "pregnancies",
    "glucose",
    "blood_pressure",
    "skin_thickness",
    "insulin",
    "bmi",
    "diabetes_pedigree_function",
    "age",
    "outcome"
]

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.h5")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")


def load_and_preprocess_data():
    """Load dataset and preprocess it."""
    print("Loading dataset...")
    try:
        # Try to load from URL
        df = pd.read_csv(DATASET_URL, header=None, names=DATASET_COLUMNS)
        print(f"Dataset loaded successfully. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading from URL: {e}")
        print("Please ensure you have internet connection or download the dataset manually.")
        raise
    
    # Display basic info
    print("\nDataset Info:")
    print(df.info())
    print("\nFirst few rows:")
    print(df.head())
    print("\nDataset statistics:")
    print(df.describe())
    
    # Handle missing values
    # In Pima Indians dataset, 0s in certain columns represent missing values
    # Replace 0s with NaN for columns where 0 is not a valid value
    columns_to_fix = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]
    for col in columns_to_fix:
        df[col] = df[col].replace(0, np.nan)
    
    print(f"\nMissing values after replacing 0s:")
    print(df.isnull().sum())
    
    # Fill missing values with median
    for col in columns_to_fix:
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)
    
    print(f"\nMissing values after imputation:")
    print(df.isnull().sum())
    
    # Separate features and target
    X = df.drop("outcome", axis=1)
    y = df["outcome"]
    
    print(f"\nFeature shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    return X, y


def build_model(input_dim):
    """Build the ANN model architecture."""
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(input_dim,)),
        layers.Dropout(0.3),
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def train_model():
    """Main training function."""
    print("=" * 60)
    print("Diabetes Prediction Model Training")
    print("=" * 60)
    
    # Load and preprocess data
    X, y = load_and_preprocess_data()
    
    # Split data
    print("\nSplitting data into train/test sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Normalize features
    print("\nNormalizing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build model
    print("\nBuilding ANN model...")
    model = build_model(input_dim=X_train_scaled.shape[1])
    print("\nModel architecture:")
    model.summary()
    
    # Train model
    print("\nTraining model...")
    history = model.fit(
        X_train_scaled,
        y_train,
        epochs=100,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    test_loss, test_accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
    print(f"\nTest Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Get predictions for detailed metrics
    y_pred_proba = model.predict(X_test_scaled, verbose=0)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("\n" + "=" * 60)
    print("Model Performance Metrics")
    print("=" * 60)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and scaler
    print("\nSaving model and scaler...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    model.save(MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")
    
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler saved to: {SCALER_PATH}")
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)
    
    return model, scaler, history


if __name__ == "__main__":
    train_model()

