import React from "react";
import "./ExplanationChart.css";
import { motion } from "framer-motion";
import { FaChartBar } from "react-icons/fa";

const ExplanationChart = ({ explanations }) => {
  if (!explanations || explanations.length === 0) {
    return (
      <div className="no-data">
        <FaChartBar size={28} />
        <p>No explanation data available</p>
      </div>
    );
  }

  return (
    <div className="explanation-container">
      <h3 className="explanation-title">
        📊 Key Feature Impact (SHAP Analysis)
      </h3>

      <div className="chart-wrapper">
        {explanations.map((item, index) => (
          <motion.div
            key={index}
            className="chart-row"
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.07 }}
          >
            <span className="feature-name">{item.feature}</span>

            <motion.div
              className="bar"
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(Math.abs(item.impact) * 60, 100)}%` }}
              transition={{ duration: 0.6 }}
            >
              <span className="impact-value">
                {item.impact.toFixed(3)}
              </span>
            </motion.div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ExplanationChart;
