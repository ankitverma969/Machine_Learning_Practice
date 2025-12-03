# src/explain.py
"""
SHAP explanation utility functions for the AI Career Guidance System.
Uses the saved shap_explainer.pkl and the sklearn preprocessing pipeline
to generate human-friendly explanations.
"""

import numpy as np
import joblib
from pathlib import Path
from src.preprocess import NUM_FEATURES, CAT_FEATURES


# -------------------------------------------------------------
# 1. PATHS
# -------------------------------------------------------------
SHAP_PATH = "../models/shap_explainer.pkl"


# -------------------------------------------------------------
# 2. LOAD SHAP EXPLAINER
# -------------------------------------------------------------
if not Path(SHAP_PATH).exists():
    raise FileNotFoundError("❌ SHAP explainer not found. Run train_model.py first.")

explainer = joblib.load(SHAP_PATH)


# -------------------------------------------------------------
# 3. GENERATE EXPLAINABILITY OUTPUT
# -------------------------------------------------------------
def get_shap_explanations(pipeline, df_preprocessed, predicted_class_index: int, top_k: int = 7):
    """
    Generate a list of SHAP explanations:
    → feature name
    → SHAP impact value (positive/negative)
    
    Args:
        pipeline: The sklearn Pipeline (preprocessor + xgboost model)
        df_preprocessed: The transformed single-row array from the preprocessor
        predicted_class_index: The index of the predicted class
        top_k: number of top features to return
    
    Returns:
        List of {feature: str, impact: float}
    """

    # SHAP returns values for each class in multi-class models
    shap_values = explainer.shap_values(df_preprocessed)
    shap_for_pred = shap_values[predicted_class_index][0]   # shape: (n_features,)

    # ---------------------------------------------------------
    # Rebuild feature names (NUM + OHE categorical)
    # ---------------------------------------------------------
    cat_feature_names = list(
        pipeline.named_steps["pre"]
        .named_transformers_["cat"]
        .get_feature_names_out(CAT_FEATURES)
    )

    feature_names = NUM_FEATURES + cat_feature_names

    # Safety: SHAP values may mismatch with feature names count due to
    # rare categorical categories not present in training
    if len(feature_names) != len(shap_for_pred):
        return [{"feature": "N/A", "impact": 0.0}]

    # ---------------------------------------------------------
    # Sort features by absolute impact
    # ---------------------------------------------------------
    sorted_idx = np.argsort(np.abs(shap_for_pred))[::-1][:top_k]

    top_features = [
        {
            "feature": feature_names[i],
            "impact": float(shap_for_pred[i])
        }
        for i in sorted_idx
    ]

    return top_features


# -------------------------------------------------------------
# DEBUG TEST
# -------------------------------------------------------------
if __name__ == "__main__":
    print("🧪 SHAP explanation module loaded successfully.")
