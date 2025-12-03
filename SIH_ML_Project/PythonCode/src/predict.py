# src/predict.py
"""
Prediction + SHAP explanation utilities for the Career Guidance ML model.
Used by FastAPI to perform real-time inference.
"""

import joblib
import numpy as np
import pandas as pd

from pathlib import Path
from src.preprocess import preprocess_input, NUM_FEATURES, CAT_FEATURES

# -------------------------------------------------------------
# 1. PATHS
# -------------------------------------------------------------
MODEL_PATH = "models/career_model.pkl"
SHAP_PATH = "models/shap_explainer.pkl"
LABEL_PATH = "models/label_mapping.pkl"

# -------------------------------------------------------------
# 2. LOAD MODEL + SHAP + LABEL ENCODER
# -------------------------------------------------------------
print("🔄 Loading ML model, SHAP explainer & label mapping...")

if not Path(MODEL_PATH).exists():
    raise FileNotFoundError("❌ career_model.pkl not found. Train the model first.")

if not Path(SHAP_PATH).exists():
    raise FileNotFoundError("❌ shap_explainer.pkl not found. Train the model first.")

if not Path(LABEL_PATH).exists():
    raise FileNotFoundError("❌ label_mapping.pkl not found. Train the model first.")

pipeline = joblib.load(MODEL_PATH)
explainer = joblib.load(SHAP_PATH)
label_encoder = joblib.load(LABEL_PATH)     # This is a LabelEncoder object

# Reverse label mapping using LabelEncoder
reverse_label_map = {i: label for i, label in enumerate(label_encoder.classes_)}

print("✅ Model + Explainer + Label Mapping loaded successfully!")

# -------------------------------------------------------------
# 3. PREDICTION FUNCTION
# -------------------------------------------------------------
def predict_single(input_dict: dict) -> dict:

    df = preprocess_input(input_dict)

    # Predict encoded label (0,1,2)
    pred_encoded = pipeline.predict(df)[0]

    # Convert to actual label string
    pred_label = reverse_label_map[pred_encoded]

    # Predict probability distribution
    probs = pipeline.predict_proba(df)[0]
    confidence = float(np.max(probs))

    # Class list (encoded)
    classes_encoded = list(range(len(label_encoder.classes_)))

    # ---------------------------------------------------------
    # SHAP Explanation
    # ---------------------------------------------------------
    df_preprocessed = pipeline.named_steps["pre"].transform(df)
    shap_values = explainer.shap_values(df_preprocessed)

    # For multi-class, shap_values is list
    shap_for_pred = shap_values[pred_encoded][0]

    # Feature names
    feature_names = (
        NUM_FEATURES
        + list(
            pipeline.named_steps["pre"]
            .named_transformers_["cat"]
            .get_feature_names_out(CAT_FEATURES)
        )
    )

    # Sort biggest contributors
    sorted_idx = np.argsort(np.abs(shap_for_pred))[::-1][:7]

    top_features = [
        {"feature": feature_names[i], "impact": float(shap_for_pred[i])}
        for i in sorted_idx
    ]

    # Build final response
    return {
        "prediction": pred_label,
        "confidence": confidence,
        "probabilities": {
            reverse_label_map[i]: float(probs[i]) for i in classes_encoded
        },
        "top_explanations": top_features
    }


# -------------------------------------------------------------
# TEST
# -------------------------------------------------------------
if __name__ == "__main__":
    print("🧪 Testing predict_single()…")

    sample = {
        "age": 16,
        "G1": 12,
        "G2": 14,
        "G3": 15,
        "studytime": 3,
        "failures": 0,
        "absences": 4,
        "sex": "F",
        "address": "U",
        "famsize": "GT3",
        "Pstatus": "T",
        "schoolsup": "yes",
        "famsup": "no",
        "paid": "no",
        "activities": "yes",
        "nursery": "yes",
        "higher": "yes",
        "internet": "yes",
        "romantic": "no"
    }

    print(predict_single(sample))
