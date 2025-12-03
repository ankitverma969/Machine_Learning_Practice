# 🎓 AI-Enhanced Career Guidance System (Supervised ML + FastAPI + MERN)

This project is a **Smart India Hackathon (SIH)–style AI system** that predicts a student’s **academic performance category** (High / Medium / Low) and provides personalized **career recommendations**, using:

- **Python Machine Learning Model**
- **FastAPI Backend (ML API)**
- **MERN Stack UI + Database**
- **SHAP Explainability**

Built using the **Math Student Performance Dataset** (Kaggle), this system ensures accurate guidance and transparent predictions.

---

# 🚀 Features

### ✅ **Supervised ML Model**
- Uses XGBoost Classifier  
- Trained on `student-mat.csv`  
- Predicts **High**, **Medium**, **Low** performance  
- Uses numeric + categorical + derived custom features  

### ✅ **Explainable AI (XAI)**
- SHAP values highlight **why** the model predicted a specific result  
- Shows top influential features for each student  

### ✅ **FastAPI Backend**
- `/predict` endpoint returns:
  - predicted label  
  - confidence score  
  - probabilities  
  - SHAP explanations  

### ✅ **MERN Integration (Frontend + Backend)**
- React collects user inputs  
- Node.js sends inputs → FastAPI  
- MongoDB stores predictions  
- UI displays prediction + recommended careers  

---

# 🧠 Project Architecture

MERN Frontend → Node Backend → FastAPI Model API → ML Pipeline → Response with SHAP


---

# 🛠 Installation & Setup

## 1️⃣ Create Virtual Environment (Required)
```bash
python -m venv venv
venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

Start server:
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
