# src/predict.py
"""
Prediction + SHAP explanation utilities for the Career Guidance ML model.
Robust input normalization: accepts either cleaned (underscore) keys or raw Excel keys.
"""

import joblib
import numpy as np
from pathlib import Path
from src.preprocess import preprocess_input  # preprocess_input expects CLEANED keys (underscore style -> maps to raw)
from src.explain import get_shap_explanations, extract_feature_names_from_pipeline

# -------------------------------------------------------------
# PATHS
# -------------------------------------------------------------
MODEL_PATH = "models/career_model.pkl"
LABEL_PATH = "models/label_mapping.pkl"
SHAP_PATH = "models/shap_explainer.pkl"

# -------------------------------------------------------------
# LOAD ARTIFACTS
# -------------------------------------------------------------
print("🔄 Loading ML model, SHAP explainer & label mapping...")

if not Path(MODEL_PATH).exists():
    raise FileNotFoundError("❌ career_model.pkl not found. Run train_model.py first.")
if not Path(LABEL_PATH).exists():
    raise FileNotFoundError("❌ label_mapping.pkl not found. Run train_model.py first.")
if not Path(SHAP_PATH).exists():
    raise FileNotFoundError("❌ shap_explainer.pkl not found. Run train_model.py first.")

pipeline = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_PATH)
explainer = joblib.load(SHAP_PATH)

reverse_label_map = {i: label for i, label in enumerate(label_encoder.classes_)}

print("✅ Model + Explainer + Label Mapping loaded successfully!")


# -------------------------------------------------------------
# FIELD MAP: cleaned (API) key -> raw Excel column name
# Keep this consistent with api/schemas.py and preprocess.py
# -------------------------------------------------------------
COLUMN_MAP = {
    "Gender": "Gender",
    "Age": "Age",
    "CGPA": "CGPA",
    "Matriculation_Percentage": "Matriculation Percentage",
    "Intermediate_Percentage": "Intermediate Percentage",
    "Data_Structures_And_Algorithm_Marks": "Data Structures And Algorithm Marks",
    "DBMS_Marks": "DBMS Marks",
    "Number_of_backlogs": "Number of backlogs",
    "Number_of_Reappears": "Number of Reappears",
    "History_of_Reappear_Backlogs": "History of Reappear/Backlogs",
    "Programming_proficiency": "Programming proficiency",
    "GitHub_total_repositories": "GitHub total repositories",
    "GitHub_commits_per_month": "GitHub commits/month",
    "Experience_with_frameworks": "Experience with frameworks",
    "English_proficiency": "English proficiency",
    "Coding_practice_hours_per_week": "Coding practice hours/week",
    "Aptitude_score": "Aptitude score",
    "Attandance": "Attandance"
}

# Helper: list of cleaned keys we accept
CLEANED_KEYS = list(COLUMN_MAP.keys())
RAW_KEYS = list(COLUMN_MAP.values())


# -------------------------------------------------------------
# INPUT NORMALIZATION HELPERS
# -------------------------------------------------------------
def _to_num_safe(x, default=0.0):
    """Convert to float if possible, else default."""
    try:
        if x is None:
            return default
        if isinstance(x, str):
            # remove extra commas, whitespace
            s = x.strip().replace(",", "")
            if s == "":
                return default
            return float(s)
        return float(x)
    except Exception:
        return default


def normalize_input_any(input_dict: dict) -> dict:
    """
    Create a normalized dict using CLEANED keys (underscore style).
    Accepts input that may contain either cleaned keys or raw excel keys.
    Returns: dict with CLEANED_KEYS as keys (missing keys omitted - preprocess fills them).
    """
    out = {}

    # lower-key mapping for fuzzy lookup
    lowered = {str(k).strip().lower(): v for k, v in input_dict.items()}

    for clean_key, raw_key in COLUMN_MAP.items():
        # prefer cleaned key if provided
        if clean_key in input_dict:
            out[clean_key] = input_dict[clean_key]
            continue

        # prefer raw key if provided
        if raw_key in input_dict:
            out[clean_key] = input_dict[raw_key]
            continue

        # fuzzy: check lowercase raw/clean names in lowered
        if raw_key.lower() in lowered:
            out[clean_key] = lowered[raw_key.lower()]
            continue
        if clean_key.lower() in lowered:
            out[clean_key] = lowered[clean_key.lower()]
            continue

        # not present: do not add (preprocess_input will add defaults)
        # but to be explicit, set sensible default for numeric-like fields
        if clean_key in {
            "Age", "CGPA", "Matriculation_Percentage", "Intermediate_Percentage",
            "Data_Structures_And_Algorithm_Marks", "DBMS_Marks",
            "Number_of_backlogs", "Number_of_Reappears",
            "GitHub_total_repositories", "GitHub_commits_per_month",
            "Coding_practice_hours_per_week", "Aptitude_score", "Attandance"
        }:
            out[clean_key] = 0
        else:
            out[clean_key] = "Unknown"

    return out


# -------------------------------------------------------------
# MAIN PREDICTION FUNCTION
# -------------------------------------------------------------
def predict_single(input_dict: dict) -> dict:
    """
    Accepts raw incoming JSON (either cleaned keys or raw Excel keys),
    normalizes to cleaned keys, calls preprocess_input (which maps cleaned -> raw),
    runs the pipeline, and returns prediction + probs + SHAP explanations.
    """
    try:
        # 1) Normalize incoming JSON to cleaned keys (underscored)
        normalized = normalize_input_any(input_dict)

        # 2) preprocess_input expects CLEANED keys and will map to raw columns the pipeline uses
        df = preprocess_input(normalized)

        # 3) run model
        pred_encoded = int(pipeline.predict(df)[0])
        pred_label = reverse_label_map[pred_encoded]

        probs = pipeline.predict_proba(df)[0]
        confidence = float(np.max(probs))

        # 4) prepare preprocessed row for SHAP (transform with pipeline.pre)
        df_preprocessed = pipeline.named_steps["pre"].transform(df)

        explanations = get_shap_explanations(
            pipeline=pipeline,
            df_preprocessed=df_preprocessed,
            predicted_class_index=pred_encoded,
            top_k=7
        )

        return {
            "prediction": pred_label,
            "confidence": confidence,
            "probabilities": {reverse_label_map[i]: float(probs[i]) for i in range(len(probs))},
            "top_explanations": explanations
        }

    except Exception as e:
        # Re-raise with context so FastAPI shows a helpful message
        raise RuntimeError(f"Prediction error: {e}") from e


# -------------------------------------------------------------
# DEBUG: quick local test
# -------------------------------------------------------------
if __name__ == "__main__":
    sample_raw = {
        # using raw (space) keys
        "Gender": "Male",
        "Age": 21,
        "CGPA": 8.1,
        "Matriculation Percentage": 88,
        "Intermediate Percentage": 86,
        "Data Structures And Algorithm Marks": 75,
        "DBMS Marks": 78,
        "Number of backlogs": 0,
        "Number of Reappears": 0,
        "History of Reappear/Backlogs": "No",
        "Programming proficiency": "Advanced",
        "GitHub total repositories": 3,
        "GitHub commits/month": 6,
        "Experience with frameworks": "React",
        "English proficiency": "Good",
        "Coding practice hours/week": 10,
        "Aptitude score": 72,
        "Attandance": 90
    }

    sample_clean = {
        # using cleaned (underscore) keys (what frontend should send)
        "Gender": "Female",
        "Age": 20,
        "CGPA": 7.9,
        "Matriculation_Percentage": 82,
        "Intermediate_Percentage": 80,
        "Data_Structures_And_Algorithm_Marks": 70,
        "DBMS_Marks": 65,
        "Number_of_backlogs": 1,
        "Number_of_Reappears": 0,
        "History_of_Reappear_Backlogs": "Yes",
        "Programming_proficiency": "Intermediate",
        "GitHub_total_repositories": 1,
        "GitHub_commits_per_month": 1,
        "Experience_with_frameworks": "Django",
        "English_proficiency": "Average",
        "Coding_practice_hours_per_week": 4,
        "Aptitude_score": 60,
        "Attandance": 85
    }

    print("Raw sample prediction:", predict_single(sample_raw))
    print("Clean sample prediction:", predict_single(sample_clean))
