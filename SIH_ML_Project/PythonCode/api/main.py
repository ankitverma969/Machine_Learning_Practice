# api/main.py
"""
FastAPI server for the AI-Enhanced Career Guidance System.
Serves ML predictions and SHAP explanations through /predict endpoint.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import Pydantic schemas
from api.schemas import StudentInput, PredictionResponse, HealthResponse

# Prediction function
from src.predict import predict_single


# ============================================================
# 1. FASTAPI SETUP
# ============================================================
app = FastAPI(
    title="AI Career Guidance System",
    description="Predicts recommended career paths for B.Tech students using ML + SHAP explainability.",
    version="2.0.0"
)

# CORS for MERN frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific domain before production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 2. HEALTH CHECK ENDPOINT
# ============================================================
@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "ok",
        "message": "AI Career Guidance API is running successfully."
    }


# ============================================================
# 3. MAIN PREDICTION ENDPOINT
# ============================================================
@app.post("/predict", response_model=PredictionResponse)
def predict_student(data: StudentInput):
    """
    Accepts student attributes (academics + skills + coding + GitHub + aptitude)
    Runs ML model inference
    Returns:
        - Recommended Career Path
        - Confidence Score
        - Probability Distribution
        - Top SHAP explanations
    """
    try:
        user_input = data.dict()  # convert to Python dict

        # ML prediction
        result = predict_single(user_input)

        # Build API structured response
        return {
            "status": "success",
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],
            "explanations": result["top_explanations"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"🔥 Prediction Failed: {str(e)}"
        )


# ============================================================
# 4. RUN SERVER (DEV MODE)
# ============================================================
if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
