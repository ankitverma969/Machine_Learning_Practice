# api/schemas.py
"""
Pydantic request and response schemas for the AI Career Guidance API.
These models ensure validation, clean API structure, and MERN compatibility.
"""

from pydantic import BaseModel
from typing import Dict, List, Optional


# -------------------------------------------------------------
# REQUEST MODEL → Student Input
# -------------------------------------------------------------
class StudentInput(BaseModel):
    # Numeric Inputs
    age: int
    G1: float
    G2: float
    G3: float = 0
    studytime: float
    failures: int
    absences: int

    # Categorical Inputs
    sex: str
    address: str
    famsize: str
    Pstatus: str
    schoolsup: str
    famsup: str
    paid: str
    activities: str
    nursery: str
    higher: str
    internet: str
    romantic: str


# -------------------------------------------------------------
# RESPONSE MODEL → SHAP Explanation
# -------------------------------------------------------------
class ExplanationItem(BaseModel):
    feature: str
    impact: float


# -------------------------------------------------------------
# RESPONSE MODEL → Prediction Output
# -------------------------------------------------------------
class PredictionResponse(BaseModel):
    status: str
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    explanations: List[ExplanationItem]


# -------------------------------------------------------------
# RESPONSE MODEL → Health Check
# -------------------------------------------------------------
class HealthResponse(BaseModel):
    status: str
    message: str
