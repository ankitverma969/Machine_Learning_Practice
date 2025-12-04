# src/preprocess.py
"""
Preprocessing for the B.Tech Career Guidance dataset.
This version correctly maps frontend clean field names to raw dataset column names.
"""

import pandas as pd


# -------------------------------------------------------------
# 1. CLEAN API NAME → RAW EXCEL COLUMN NAME MAP
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


# -------------------------------------------------------------
# 2. RENAME CLEAN INPUT → RAW DATASET NAMES
# -------------------------------------------------------------
def rename_to_raw_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renames cleaned API fields into raw Excel dataset field names."""
    reverse_map = {clean: raw for clean, raw in COLUMN_MAP.items()}
    return df.rename(columns=reverse_map)


# -------------------------------------------------------------
# 3. MAIN PREPROCESS FUNCTION
# -------------------------------------------------------------
def preprocess_input(data: dict) -> pd.DataFrame:
    """Convert API JSON → clean DataFrame → rename → ready for model."""
    
    df = pd.DataFrame([data])

    # Remove Name if frontend sends it
    if "Name" in df.columns:
        df = df.drop(columns=["Name"])

    # Rename clean → raw
    df = rename_to_raw_columns(df)

    # Fill missing columns with 0 or "Unknown"
    for raw_col in COLUMN_MAP.values():
        if raw_col not in df.columns:
            df[raw_col] = 0  # or "Unknown" for categorical but model handles automatically

    # Ensure no missing values
    df = df.fillna(0)

    return df


# -------------------------------------------------------------
# DEBUG
# -------------------------------------------------------------
if __name__ == "__main__":
    sample = {
        "Gender": "Male",
        "Age": 20,
        "CGPA": 8.5,
        "Matriculation_Percentage": 85,
        "Intermediate_Percentage": 82,
        "Data_Structures_And_Algorithm_Marks": 78,
        "DBMS_Marks": 80,
        "Number_of_backlogs": 0,
        "Number_of_Reappears": 0,
        "History_of_Reappear_Backlogs": "No",
        "Programming_proficiency": "Advanced",
        "GitHub_total_repositories": 5,
        "GitHub_commits_per_month": 8,
        "Experience_with_frameworks": "React",
        "English_proficiency": "Good",
        "Coding_practice_hours_per_week": 10,
        "Aptitude_score": 72,
        "Attandance": 90
    }

    print(preprocess_input(sample))
