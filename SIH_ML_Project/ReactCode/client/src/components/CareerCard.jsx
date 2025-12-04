import React from "react";
import "./CareerCard.css";
import { motion } from "framer-motion";
import { FaUserGraduate, FaCheckCircle, FaChartLine } from "react-icons/fa";

const CareerCard = ({ result }) => {
  if (!result) return null;

  const { prediction, confidence, probabilities } = result;

  return (
    <motion.div
      className="career-card"
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className="career-header">
        <FaUserGraduate className="career-icon" />
        <h2>Your AI-Predicted Career Path</h2>
      </div>

      <motion.div
        className="career-highlight"
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
      >
        <h1 className="career-role">{prediction}</h1>
        <p className="career-confidence">
          Confidence Score: <strong>{(confidence * 100).toFixed(1)}%</strong>
        </p>
      </motion.div>

      {/* Probabilities Section */}
      <div className="probability-section">
        <h3>📊 Model Probability Breakdown</h3>
        <div className="probability-bars">
          {Object.keys(probabilities).map((role, idx) => (
            <div key={idx} className="prob-row">
              <span className="prob-label">{role}</span>
              
              <div className="prob-bar">
                <motion.div
                  className="prob-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${probabilities[role] * 100}%` }}
                  transition={{ duration: 0.8 }}
                ></motion.div>
              </div>

              <span className="prob-value">
                {(probabilities[role] * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Summary Section */}
      <div className="summary-section">
        <FaCheckCircle className="summary-icon" />
        <p>
          This prediction is generated using your academic, coding skills, GitHub activity,
          aptitude, and overall performance metrics.  
        </p>
      </div>
    </motion.div>
  );
};

export default CareerCard;
