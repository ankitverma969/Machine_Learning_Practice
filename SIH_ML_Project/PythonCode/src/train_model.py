# src/train_model.py
"""
Train model for AI-Enhanced Career Guidance using B.Tech dataset.
Automatically generates 'Recommended Career' target labels using rule-based logic.
Uses ALL columns (except Name) as model features.
Saves: career_model.pkl, label_mapping.pkl, shap_explainer.pkl
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
import warnings
warnings.filterwarnings("ignore")


# ================================================================
# 1. CONFIG
# ================================================================
DATA_PATH = "../data/BTech_Student_DatasetFinalOk.xlsx"
MODEL_OUTPUT = "../models/career_model.pkl"
LABEL_OUTPUT = "../models/label_mapping.pkl"
SHAP_OUTPUT = "../models/shap_explainer.pkl"
EXPORT_WITH_LABELS = "../data/BTech_Student_Dataset_with_labels.csv"


# ================================================================
# 2. LOAD DATA
# ================================================================
print("🔄 Loading dataset...")
df = pd.read_excel(DATA_PATH)
df.columns = [c.strip() for c in df.columns]

print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

if "Name" in df.columns:
    df = df.drop(columns=["Name"])
    print("🗑 Removed 'Name' column")


# ================================================================
# 3. SAFE NUMERIC CONVERSION
# ================================================================
def to_num(x, default=0.0):
    try:
        if pd.isna(x):
            return default
        return float(x)
    except:
        return default


# Convert all numeric-like fields properly
NUMERIC_FIELDS = [
    "CGPA", "Matriculation Percentage", "Intermediate Percentage",
    "Data Structures And Algorithm Marks", "DBMS Marks",
    "GitHub total repositories", "GitHub commits/month",
    "Coding practice hours/week", "Aptitude score", "Attandance",
    "Number of backlogs", "Number of Reappears"
]

for col in NUMERIC_FIELDS:
    if col in df.columns:
        df[col] = df[col].apply(to_num)


# ================================================================
# 4. GENERATE TARGET LABEL (Recommended Career)
# ================================================================
def generate_career(row):
    dsa = to_num(row.get("Data Structures And Algorithm Marks", 0))
    dbms = to_num(row.get("DBMS Marks", 0))
    cgpa = to_num(row.get("CGPA", 0))
    repos = to_num(row.get("GitHub total repositories", 0))
    commits = to_num(row.get("GitHub commits/month", 0))
    coding = to_num(row.get("Coding practice hours/week", 0))
    aptitude = to_num(row.get("Aptitude score", 0))
    
    frameworks = str(row.get("Experience with frameworks", "")).lower()
    prof = str(row.get("Programming proficiency", "")).lower()

    # --- AI / ML Engineer ---
    if aptitude >= 70 and cgpa >= 7.5 and dsa >= 65:
        return "AI/ML Engineer"

    # --- Software Engineer ---
    if dsa >= 75 and coding >= 8 and (repos >= 2 or commits >= 4):
        return "Software Engineer"

    # --- Web Developer ---
    if any(f in frameworks for f in ["react", "angular", "django", "node"]) and coding >= 5:
        return "Web Developer"

    # --- Data Analyst ---
    if dbms >= 75 and aptitude >= 65:
        return "Data Analyst"

    # --- DevOps Engineer ---
    if any(k in frameworks for k in ["devops", "docker", "kubernetes", "aws", "cloud"]) and repos >= 2:
        return "DevOps Engineer"

    # --- Cyber Security ---
    if "security" in prof or "cyber" in prof:
        return "Cyber Security Engineer"

    # FALLBACKS
    if dsa >= 70:
        return "Software Engineer"
    if dbms >= 70:
        return "Data Analyst"

    return "Software Engineer"


df["Recommended Career"] = df.apply(generate_career, axis=1)
print("📌 Career labels distribution:\n", df["Recommended Career"].value_counts())


# ================================================================
# 5. FEATURE SELECTION
# ================================================================
y = df["Recommended Career"]
X = df.drop(columns=["Recommended Career"])

numeric_cols = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]
categorical_cols = [c for c in X.columns if c not in numeric_cols]

print(f"📊 Numeric columns: {len(numeric_cols)}")
print(f"📦 Categorical columns: {len(categorical_cols)}")


# ================================================================
# 6. LABEL ENCODER
# ================================================================
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print("🏷 Classes:", label_encoder.classes_)


# ================================================================
# 7. PREPROCESSING + MODEL
# ================================================================
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
])

model = xgb.XGBClassifier(
    n_estimators=250,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="mlogloss",
    random_state=42
)

pipeline = Pipeline([
    ("pre", preprocessor),
    ("clf", model)
])


# ================================================================
# 8. TRAIN / TEST SPLIT
# ================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
)

print(f"📘 Training samples = {X_train.shape[0]}")
print(f"📙 Test samples = {X_test.shape[0]}")


# ================================================================
# 9. TRAIN MODEL
# ================================================================
print("🚀 Training model...")
pipeline.fit(X_train, y_train)
print("🎉 Training complete!")


# ================================================================
# 10. EVALUATE
# ================================================================
preds = pipeline.predict(X_test)
print("\n📊 Classification Report:\n", classification_report(y_test, preds))
print("\n🔢 Confusion Matrix:\n", confusion_matrix(y_test, preds))


# ================================================================
# 11. SAVE ARTIFACTS
# ================================================================
Path("../models").mkdir(exist_ok=True)

joblib.dump(pipeline, MODEL_OUTPUT)
print(f"💾 Saved model → {MODEL_OUTPUT}")

joblib.dump(label_encoder, LABEL_OUTPUT)
print(f"💾 Saved label encoder → {LABEL_OUTPUT}")

print("🔍 Training SHAP explainer...")
explainer = shap.TreeExplainer(pipeline.named_steps["clf"])
joblib.dump(explainer, SHAP_OUTPUT)
print(f"💾 Saved SHAP explainer → {SHAP_OUTPUT}")

df.to_csv(EXPORT_WITH_LABELS, index=False)
print(f"📄 Exported labeled dataset → {EXPORT_WITH_LABELS}")

print("\n✅ Training pipeline completed successfully!")
