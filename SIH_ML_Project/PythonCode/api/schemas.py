# api/schemas.py
"""
Pydantic request + response schemas for AI Career Guidance (B.Tech Version)
Updated to match NEW dataset fields.
"""

from pydantic import BaseModel
from typing import Dict, List


# -------------------------------------------------------------
# REQUEST MODEL → Student Input (Updated for B.Tech dataset)
# -------------------------------------------------------------
class StudentInput(BaseModel):
    Gender: str
    Age: int
    CGPA: float
    Matriculation_Percentage: float
    Intermediate_Percentage: float

    Data_Structures_And_Algorithm_Marks: float
    DBMS_Marks: float

    Number_of_backlogs: int
    Number_of_Reappears: int
    History_of_Reappears_Backlogs: str

    Programming_proficiency: str
    GitHub_total_repositories: int
    GitHub_commits_per_month: int
    Experience_with_frameworks: str
    English_proficiency: str

    Coding_practice_hours_per_week: float
    Aptitude_score: float
    Attandance: float


# -------------------------------------------------------------
# SHAP Explanation Model
# -------------------------------------------------------------
class ExplanationItem(BaseModel):
    feature: str
    impact: float


# -------------------------------------------------------------
# PREDICTION RESPONSE MODEL
# -------------------------------------------------------------
class PredictionResponse(BaseModel):
    status: str
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    explanations: List[ExplanationItem]


# -------------------------------------------------------------
# HEALTH CHECK MODEL
# -------------------------------------------------------------
class HealthResponse(BaseModel):
    status: str
    message: str
