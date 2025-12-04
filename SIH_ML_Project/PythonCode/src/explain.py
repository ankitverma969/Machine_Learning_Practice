# src/explain.py
"""
SHAP explanation utilities for the AI Career Guidance System.

This version:
 - extracts numeric + categorical (one-hot) feature names from the trained pipeline robustly,
 - supports cases where categorical transformer or OHE is absent,
 - returns top-k SHAP feature impacts for the predicted class.
"""

import numpy as np
import joblib
from pathlib import Path
from typing import List, Dict

SHAP_PATH = "models/shap_explainer.pkl"

if not Path(SHAP_PATH).exists():
    raise FileNotFoundError("❌ SHAP explainer not found. Run train_model.py first.")

explainer = joblib.load(SHAP_PATH)


def _get_column_transformer(pre):
    """
    Return the ColumnTransformer object (pre). This is for clarity/readability.
    Assumes the pipeline has a step named 'pre' (ColumnTransformer).
    """
    return pre


def _numeric_feature_names(pre) -> List[str]:
    """
    Attempt to extract numeric feature names from ColumnTransformer.
    """
    # Many ColumnTransformer objects store the original column names in the transformers list
    for name, transformer, cols in getattr(pre, "transformers", []):
        # Heuristic: scaler/num transformer often named 'num' or contains StandardScaler
        if name == "num" or hasattr(transformer, "__class__") and "StandardScaler" in transformer.__class__.__name__:
            return list(cols)
    # fallback: try to access transformers_[0][2]
    try:
        return list(pre.transformers_[0][2])
    except Exception:
        return []


def _categorical_feature_names(pre) -> List[str]:
    """
    Expand categorical columns using the fitted OneHotEncoder (if present).
    Returns a list of one-hot encoded names (like 'col__val').
    """
    # First try to find a transformer named 'cat'
    cat_cols = None
    cat_encoder = None

    # Look into named_transformers_ if available
    if hasattr(pre, "named_transformers_") and "cat" in pre.named_transformers_:
        cat_encoder = pre.named_transformers_["cat"]
        # find original cat column list via transformers if possible
        for name, transformer, cols in getattr(pre, "transformers", []):
            if name == "cat":
                cat_cols = list(cols)
                break

    # If not found by name, search for OneHotEncoder in transformers
    if cat_encoder is None:
        for name, transformer, cols in getattr(pre, "transformers", []):
            if transformer is None:
                continue
            tname = transformer.__class__.__name__.lower()
            if "onehotencoder" in tname or "onehot" in tname:
                cat_encoder = transformer
                cat_cols = list(cols)
                break

    if cat_encoder is None or cat_cols is None:
        return []

    # Try get_feature_names_out (sklearn >= 1.0)
    try:
        return list(cat_encoder.get_feature_names_out(cat_cols))
    except Exception:
        # Fallback: attempt to build names from categories_ if available
        feature_names = []
        try:
            categories = getattr(cat_encoder, "categories_", None)
            if categories is not None:
                for col, cats in zip(cat_cols, categories):
                    for val in cats:
                        feature_names.append(f"{col}__{val}")
                return feature_names
        except Exception:
            pass

    return []


def extract_feature_names_from_pipeline(pipeline) -> List[str]:
    """
    Extracts the list of transformed feature names (numeric + categorical one-hot)
    from the pipeline's ColumnTransformer ('pre' step).
    """
    if "pre" not in pipeline.named_steps:
        # If there's no preprocessor step named 'pre', attempt to find the ColumnTransformer
        # in the pipeline steps
        for name, step in pipeline.named_steps.items():
            # try to detect ColumnTransformer by attribute
            if hasattr(step, "transformers"):
                pre = step
                break
        else:
            raise RuntimeError("Cannot find ColumnTransformer in pipeline (expected step 'pre').")
    else:
        pre = pipeline.named_steps["pre"]

    numeric = _numeric_feature_names(pre)
    categorical = _categorical_feature_names(pre)

    return numeric + categorical


def get_shap_explanations(pipeline, df_preprocessed, predicted_class_index: int, top_k: int = 7) -> List[Dict]:
    """
    Produce top-k SHAP explanations for the predicted class.

    Args:
        pipeline: trained sklearn Pipeline (must have 'pre' ColumnTransformer)
        df_preprocessed: preprocessed array (1 x n_features) produced by pipeline.named_steps['pre'].transform(df)
        predicted_class_index: int index of predicted class
        top_k: number of top features to return

    Returns:
        List of dicts: {"feature": <name>, "impact": <float>}
    """
    # shap_values may be list (multi-class) or array (binary/regression)
    shap_values = explainer.shap_values(df_preprocessed)

    # Handle several shap output shapes robustly
    try:
        # If multi-class, shap_values is list-like where each element is (n_samples, n_features)
        if isinstance(shap_values, (list, tuple)):
            shap_for_pred = shap_values[predicted_class_index][0]
        else:
            # binary/regression: shap_values is (n_samples, n_features)
            shap_for_pred = shap_values[0]
    except Exception:
        return [{"feature": "SHAP_unavailable", "impact": 0.0}]

    feature_names = extract_feature_names_from_pipeline(pipeline)

    if len(feature_names) != len(shap_for_pred):
        # return an informative message rather than crashing
        return [{
            "feature": f"FEATURE_MISMATCH (expected {len(feature_names)} names, got {len(shap_for_pred)})",
            "impact": 0.0
        }]

    sorted_idx = np.argsort(np.abs(shap_for_pred))[::-1][:top_k]

    return [
        {"feature": feature_names[i], "impact": float(shap_for_pred[i])}
        for i in sorted_idx
    ]


if __name__ == "__main__":
    print("✅ SHAP explanation module loaded successfully.")
