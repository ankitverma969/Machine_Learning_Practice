# src/preprocess.py
"""
Preprocessing utilities for the Math dataset (student-mat.csv)
Used by both training (train_model.py) and inference (predict.py).
"""

import pandas as pd
import numpy as np


# -------------------------------------------------------------
# 1. FEATURE LISTS (shared with training + inference)
# -------------------------------------------------------------
NUM_FEATURES = [
    "age", "G1", "G2", "studytime", "failures", "absences",
    "performance_trend", "final_estimate",
    "engagement_score", "academic_consistency"
]

CAT_FEATURES = [
    "sex", "address", "famsize", "Pstatus",
    "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic"
]


# -------------------------------------------------------------
# 2. LOAD RAW DATA (IMPORTANT: sep=';')
# -------------------------------------------------------------
def load_raw(csv_path: str):
    """
    Load the raw math dataset from CSV.
    Student Performance dataset uses semicolon (;) separator.
    """
    df = pd.read_csv(csv_path, sep=";")
    return df


# -------------------------------------------------------------
# 3. DERIVED FEATURE GENERATION
# -------------------------------------------------------------
def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create required derived features.
    Must match logic used in train_model.py.
    """

    required_cols = ["G1", "G2", "G3", "studytime", "absences"]

    # Ensure all required columns exist (for prediction API)
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    # performance trend (improvement from G1 → G2)
    df["performance_trend"] = df["G2"] - df["G1"]

    # final estimated score
    df["final_estimate"] = (df["G1"] + df["G2"]) / 2

    # engagement score (studytime × attendance-like factor)
    df["engagement_score"] = df["studytime"] * (20 - df["absences"])

    # academic consistency (variance in grades)
    df["academic_consistency"] = df[["G1", "G2", "G3"]].std(axis=1)
    df["academic_consistency"] = df["academic_consistency"].fillna(0)

    return df


# -------------------------------------------------------------
# 4. SELECT FEATURES FOR MODEL
# -------------------------------------------------------------
def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select final ML features used by the sklearn pipeline.
    Auto-add missing categorical fields during FastAPI inference.
    """
    needed = NUM_FEATURES + CAT_FEATURES

    for col in needed:
        if col not in df.columns:
            df[col] = "none" if col in CAT_FEATURES else 0

    return df[needed]


# -------------------------------------------------------------
# 5. MAIN PREPROCESS FUNCTION (called by API)
# -------------------------------------------------------------
def preprocess_input(data: dict) -> pd.DataFrame:
    """
    Convert API JSON → dataframe → add derived features → select features.
    """

    df = pd.DataFrame([data])

    # Add derived numeric features
    df = add_derived_features(df)

    # Select final ML feature columns
    df = select_features(df)

    return df


# -------------------------------------------------------------
# DEBUG TEST
# -------------------------------------------------------------
if __name__ == "__main__":
    print("🧪 Testing preprocess.py...")

    # A realistic test sample
    sample = {
        "age": 16,
        "G1": 12,
        "G2": 14,
        "G3": 15,
        "studytime": 2,
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

    processed = preprocess_input(sample)
    print(processed.head())
