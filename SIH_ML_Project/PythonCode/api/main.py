# api/main.py
"""
FastAPI server for the AI-Enhanced Career Guidance System.
Serves ML predictions and SHAP explanations through /predict endpoint.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import schemas
from api.schemas import StudentInput, PredictionResponse, HealthResponse

# Prediction function
from src.predict import predict_single


# -------------------------------------------------------------
# 1. FASTAPI APP SETUP
# -------------------------------------------------------------
app = FastAPI(
    title="AI Career Guidance System",
    description="Predicts student performance category and provides career recommendations.",
    version="1.0.0"
)

# Allow MERN frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# 2. HEALTH CHECK ENDPOINT
# -------------------------------------------------------------
@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok", "message": "API is running."}


# -------------------------------------------------------------
# 3. MAIN ML PREDICTION ENDPOINT
# -------------------------------------------------------------
@app.post("/predict", response_model=PredictionResponse)
def predict_student(data: StudentInput):
    """
    Accept student academic + behavior data,
    run ML model inference,
    return prediction + confidence + SHAP explanations.
    """
    try:
        input_dict = data.dict()
        result = predict_single(input_dict)

        return {
            "status": "success",
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],
            "explanations": result["top_explanations"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


# -------------------------------------------------------------
# 4. RUN SERVER (DEV MODE)
# -------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
