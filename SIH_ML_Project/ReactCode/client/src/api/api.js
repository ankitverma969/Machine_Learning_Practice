// client/src/api/api.js
// Direct communication between React UI and your FastAPI ML backend

const FASTAPI_BASE = "http://localhost:8000";   // Your ML API

// Generic POST request
export async function sendPrediction(data) {
  try {
    const res = await fetch(`${FASTAPI_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) {
      throw new Error(`Prediction Failed: ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    console.error("API Error:", err);
    throw err;
  }
}

export default {
  sendPrediction,
};
