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
    # ---- Numeric features ----
    dsa         = to_num(row.get("Data Structures And Algorithm Marks", 0))
    dbms        = to_num(row.get("DBMS Marks", 0))
    cgpa        = to_num(row.get("CGPA", 0))
    repos       = to_num(row.get("GitHub total repositories", 0))
    commits     = to_num(row.get("GitHub commits/month", 0))
    coding      = to_num(row.get("Coding practice hours/week", 0))
    aptitude    = to_num(row.get("Aptitude score", 0))
    backlogs    = to_num(row.get("Number of backlogs", 0))
    reappears   = to_num(row.get("Number of Reappears", 0))
    attendance  = to_num(row.get("Attandance", 0))

    # ---- English proficiency (dropdown text -> numeric) ----
    english_raw = str(row.get("English proficiency", "Fair")).strip().lower()
    english_map = {
        "poor": 40,
        "fair": 60,
        "good": 80,
        "excellent": 95,
    }
    english = english_map.get(english_raw, 60)   # default to "Fair"

    # ---- Text features ----
    # "Experience with frameworks" can be comma/semicolon separated
    frameworks_text = str(row.get("Experience with frameworks", "")).lower()
    frameworks = [
        f.strip()
        for f in frameworks_text.replace(",", ";").split(";")
        if f.strip()
    ]
    prog_prof = str(row.get("Programming proficiency", "")).lower()

    # ---- Score container ----
    scores = {
        "AI/ML Engineer": 0,
        "Software Engineer": 0,
        "Web Developer": 0,
        "Data Analyst": 0,
        "DevOps Engineer": 0,
        "Cyber Security Engineer": 0,
    }

    # ---------- COMMON SIGNALS ----------
    if cgpa >= 8.0:
        for r in scores:
            scores[r] += 1
    if cgpa >= 8.5:
        for r in scores:
            scores[r] += 1

    if backlogs > 0 or reappears > 0:
        for r in scores:
            scores[r] -= 1
    if backlogs >= 3 or reappears >= 3:
        for r in scores:
            scores[r] -= 1
    if attendance < 70:
        for r in scores:
            scores[r] -= 1

    if english >= 70:
        for r in scores:
            scores[r] += 1
    if aptitude >= 70:
        for r in scores:
            scores[r] += 1

    # ---------- AI / ML Engineer ----------
    if dsa >= 80:
        scores["AI/ML Engineer"] += 1
    if "python" in frameworks:
        scores["AI/ML Engineer"] += 1
    if any(f in frameworks for f in ["numpy", "pandas", "tensorflow", "pytorch", "sklearn"]):
        scores["AI/ML Engineer"] += 2
    if coding >= 8:
        scores["AI/ML Engineer"] += 1
    if aptitude >= 85 and cgpa >= 8.5 and dsa >= 85:
        scores["AI/ML Engineer"] += 2

    # ---------- Software Engineer ----------
    if dsa >= 75:
        scores["Software Engineer"] += 2
    if coding >= 10:
        scores["Software Engineer"] += 2
    if repos >= 2:
        scores["Software Engineer"] += 1
    if commits >= 4:
        scores["Software Engineer"] += 1
    if any(lang in frameworks for lang in ["java", "c++", "c#", "golang"]):
        scores["Software Engineer"] += 1
    if "advanced" in prog_prof or "intermediate" in prog_prof:
        scores["Software Engineer"] += 1

    # ---------- Web Developer ----------
    if any(f in frameworks for f in [
        "html", "css", "javascript", "react", "angular",
        "vue", "django", "node", "next.js", "express"
    ]):
        scores["Web Developer"] += 2
    if coding >= 6:
        scores["Web Developer"] += 1
    if repos >= 2:
        scores["Web Developer"] += 1
    if commits >= 4:
        scores["Web Developer"] += 1

    # ---------- Data Analyst ----------
    if dbms >= 75:
        scores["Data Analyst"] += 2
    if aptitude >= 65:
        scores["Data Analyst"] += 1
    if any(f in frameworks for f in ["excel", "power bi", "tableau", "sql"]):
        scores["Data Analyst"] += 2
    if any(f in frameworks for f in ["numpy", "pandas"]):
        scores["Data Analyst"] += 1
    if coding >= 4:
        scores["Data Analyst"] += 1

    # ---------- DevOps Engineer ----------
    if any(k in frameworks for k in [
        "devops", "docker", "kubernetes", "k8s", "aws",
        "azure", "gcp", "jenkins", "ci/cd", "cloud"
    ]):
        scores["DevOps Engineer"] += 3
    if repos >= 2:
        scores["DevOps Engineer"] += 1
    if commits >= 5:
        scores["DevOps Engineer"] += 1
    if aptitude >= 70:
        scores["DevOps Engineer"] += 1

    # ---------- Cyber Security Engineer ----------
    if any(k in frameworks for k in [
        "security", "cyber", "network", "penetration testing",
        "ethical hacking", "kali"
    ]):
        scores["Cyber Security Engineer"] += 3
    if "security" in prog_prof or "cyber" in prog_prof:
        scores["Cyber Security Engineer"] += 2
    if aptitude >= 70:
        scores["Cyber Security Engineer"] += 1

    # ---------- FINAL SELECTION ----------
    best_role = max(scores, key=scores.get)
    best_score = scores[best_role]

    if best_score <= 0:
        return "Software Engineer"  # very weak signals: safe default

    return best_role


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
