import React, { useState } from "react";
import PredictionForm from "./components/PredictionForm";
import ExplanationChart from "./components/ExplanationChart";
import Recommendations from "./components/Recommendations";
import "./App.css";

const App = () => {
  const [mlResult, setMlResult] = useState(null);

  return (
    <div className="app-container">

      {/* HEADER */}
      <header className="header">
        <h1>🎓 AI-Enhanced Career Guidance System</h1>
        <p>Analyze student performance using ML + provide smart career pathways</p>
      </header>

      <div className="layout">
        {/* LEFT SIDE (FORM) */}
        <div className="left-panel">
          <PredictionForm onResult={setMlResult} />
        </div>

        {/* MIDDLE: SHAP Feature Impact */}
        <div className="middle-panel">
          {mlResult ? (
            <ExplanationChart explanations={mlResult.explanations} />
          ) : (
            <div className="placeholder">
              <p>📊 No explanation data available</p>
            </div>
          )}
        </div>

        {/* RIGHT SIDE: Recommendations */}
        <div className="right-panel">
          <Recommendations
            prediction={mlResult?.prediction}
            confidence={mlResult?.confidence}
            shap={mlResult?.explanations}
          />
        </div>
      </div>

    </div>
  );
};

export default App;
