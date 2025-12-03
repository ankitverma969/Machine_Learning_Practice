# src/train_model.py
"""
Train the AI Career Guidance Model using ONLY the Math dataset.
This script prepares labels, preprocesses features, trains an ML model,
evaluates it, and saves the trained pipeline + SHAP explainer + label mapping.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
import shap

# -------------------------------------------------------------
# 1. CONFIG
# -------------------------------------------------------------
DATA_PATH = "../data/student-mat.csv"     # change if needed
MODEL_OUTPUT = "../models/career_model.pkl"
SHAP_OUTPUT = "../models/shap_explainer.pkl"
LABEL_MAP_OUTPUT = "../models/label_mapping.pkl"

# -------------------------------------------------------------
# 2. LOAD DATA
# -------------------------------------------------------------
print("🔄 Loading dataset...")
df = pd.read_csv(DATA_PATH, sep=";")

print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")


# -------------------------------------------------------------
# 3. CREATE LABEL Y = High / Medium / Low based on G3
# -------------------------------------------------------------
def label_performance(g3):
    if g3 >= 15:
        return "High"
    elif g3 >= 10:
        return "Medium"
    else:
        return "Low"

df["performance_label"] = df["G3"].apply(label_performance)

print("🎯 Created target labels (High, Medium, Low)")


# -------------------------------------------------------------
# 4. LABEL ENCODING (string → numbers)
# -------------------------------------------------------------
label_encoder = LabelEncoder()
df["label_encoded"] = label_encoder.fit_transform(df["performance_label"])

print("📌 Label mapping:", dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))))


# -------------------------------------------------------------
# 5. FEATURE ENGINEERING
# -------------------------------------------------------------
print("⚙️  Generating derived features...")

df["performance_trend"] = df["G2"] - df["G1"]
df["final_estimate"] = (df["G1"] + df["G2"]) / 2
df["engagement_score"] = df["studytime"] * (20 - df["absences"])
df["academic_consistency"] = df[["G1", "G2", "G3"]].std(axis=1)

NUM_FEATURES = [
    "age", "G1", "G2", "studytime", "failures", "absences",
    "performance_trend", "final_estimate",
    "engagement_score", "academic_consistency"
]

CAT_FEATURES = [
    "sex", "address", "famsize", "Pstatus", "schoolsup", "famsup",
    "paid", "activities", "nursery", "higher", "internet", "romantic"
]


X = df[NUM_FEATURES + CAT_FEATURES]
y = df["label_encoded"]

print("📌 Features selected:")
print(f"Numeric: {len(NUM_FEATURES)}, Categorical: {len(CAT_FEATURES)}")
print(f"Total features: {X.shape[1]}")


# -------------------------------------------------------------
# 6. PREPROCESSING PIPELINE
# -------------------------------------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), NUM_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_FEATURES)
    ]
)


# -------------------------------------------------------------
# 7. MODEL: XGBoost Classifier
# -------------------------------------------------------------
model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    eval_metric="mlogloss",
    random_state=42
)

pipeline = Pipeline(steps=[
    ("pre", preprocessor),
    ("clf", model)
])


# -------------------------------------------------------------
# 8. TRAIN / TEST SPLIT
# -------------------------------------------------------------
print("🔀 Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"Train size: {X_train.shape[0]}")
print(f"Test size : {X_test.shape[0]}")


# -------------------------------------------------------------
# 9. TRAIN MODEL
# -------------------------------------------------------------
print("🚀 Training model...")
pipeline.fit(X_train, y_train)
print("🎉 Training complete!")


# -------------------------------------------------------------
# 10. EVALUATION
# -------------------------------------------------------------
print("\n📊 MODEL EVALUATION:")
preds = pipeline.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, preds))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, preds))


# -------------------------------------------------------------
# 11. SAVE MODEL + LABEL MAP
# -------------------------------------------------------------
print(f"\n💾 Saving model → {MODEL_OUTPUT}")
Path("../models").mkdir(exist_ok=True)
joblib.dump(pipeline, MODEL_OUTPUT)

print(f"💾 Saving label mapping → {LABEL_MAP_OUTPUT}")
joblib.dump(label_encoder, LABEL_MAP_OUTPUT)

print("Model + Label Encoder saved!")


# -------------------------------------------------------------
# 12. SAVE SHAP EXPLAINER
# -------------------------------------------------------------
print("\n🔍 Generating SHAP explainer...")

# Preprocess training data
X_train_preprocessed = pipeline.named_steps["pre"].transform(X_train)

explainer = shap.TreeExplainer(pipeline.named_steps["clf"])
joblib.dump(explainer, SHAP_OUTPUT)

print(f"SHAP explainer saved → {SHAP_OUTPUT}")

print("\n✅ Training pipeline completed successfully!")
