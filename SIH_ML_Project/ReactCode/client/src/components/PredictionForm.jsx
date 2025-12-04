import React, { useState } from "react";
import "./PredictionForm.css";
import { motion } from "framer-motion";
import { sendPrediction } from "../api/api";

const PredictionForm = ({ onResult }) => {
  const [formData, setFormData] = useState({
    Gender: "",
    Age: "",
    CGPA: "",
    Matriculation_Percentage: "",
    Intermediate_Percentage: "",

    Data_Structures_And_Algorithm_Marks: "",
    DBMS_Marks: "",

    Number_of_backlogs: "",
    Number_of_Reappears: "",
    History_of_Reappears_Backlogs: "",

    Programming_proficiency: "",
    GitHub_total_repositories: "",
    GitHub_commits_per_month: "",
    Experience_with_frameworks: "",
    English_proficiency: "",

    Coding_practice_hours_per_week: "",
    Aptitude_score: "",
    Attandance: ""
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      console.log("📤 Sending Payload to ML Model:", formData);

      const result = await sendPrediction(formData);
      console.log("📥 ML Model Response:", result);

      onResult(result);
    } catch (err) {
      console.error("❌ Prediction Error:", err);
      alert(err.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="prediction-form-container"
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <h2 className="form-title">🎓 AI Career Guidance – Student Analysis Form</h2>

      <form className="prediction-form" onSubmit={handleSubmit}>

        {/* -------------------------- PERSONAL --------------------------- */}
        <div className="form-section">
          <h3>Personal Details</h3>

          <div className="row">
            <select name="Gender" onChange={handleChange} required>
              <option value="">Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>

            <input type="number" name="Age" placeholder="Age" onChange={handleChange} required />
          </div>
        </div>

        {/* -------------------------- ACADEMICS --------------------------- */}
        <div className="form-section">
          <h3>Academic Details</h3>

          <div className="row">
            <input type="number" step="0.1" name="CGPA" placeholder="CGPA" onChange={handleChange} />
            <input type="number" name="Matriculation_Percentage" placeholder="Matriculation %" onChange={handleChange} />
            <input type="number" name="Intermediate_Percentage" placeholder="Intermediate %" onChange={handleChange} />
          </div>

          <div className="row">
            <input type="number" name="Data_Structures_And_Algorithm_Marks" placeholder="DSA Marks" onChange={handleChange} />
            <input type="number" name="DBMS_Marks" placeholder="DBMS Marks" onChange={handleChange} />

            <input type="number" name="Number_of_backlogs" placeholder="Backlogs" onChange={handleChange} />
            <input type="number" name="Number_of_Reappears" placeholder="Reappears" onChange={handleChange} />
          </div>

          <textarea
            name="History_of_Reappears_Backlogs"
            placeholder="History of Reappears / Backlogs"
            onChange={handleChange}
          ></textarea>
        </div>

        {/* -------------------------- SKILLS --------------------------- */}
        <div className="form-section">
          <h3>Skills & Experience</h3>

          <div className="row">
            <select name="Programming_proficiency" onChange={handleChange}>
              <option value="">Programming Proficiency</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>

            <input type="number" name="GitHub_total_repositories" placeholder="GitHub Repositories" onChange={handleChange} />
            <input type="number" name="GitHub_commits_per_month" placeholder="Commits per Month" onChange={handleChange} />
          </div>

          <div className="row">
            <select name="Experience_with_frameworks" onChange={handleChange}>
              <option value="">Framework Experience</option>
              <option value="None">None</option>
              <option value="React">React</option>
              <option value="Node">Node</option>
              <option value="Django">Django</option>
              <option value="Flutter">Flutter</option>
            </select>

            <select name="English_proficiency" onChange={handleChange}>
              <option value="">English Proficiency</option>
              <option value="Poor">Poor</option>
              <option value="Average">Average</option>
              <option value="Good">Good</option>
              <option value="Excellent">Excellent</option>
            </select>

            <input type="number" name="Coding_practice_hours_per_week" placeholder="Coding Hours/Week" onChange={handleChange} />
          </div>

          <div className="row">
            <input type="number" name="Aptitude_score" placeholder="Aptitude Score" onChange={handleChange} />
            <input type="number" name="Attandance" placeholder="Attendance (%)" onChange={handleChange} />
          </div>
        </div>

        {/* -------------------------- BUTTON --------------------------- */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="submit-btn"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Predict Career Path 🚀"}
        </motion.button>

      </form>
    </motion.div>
  );
};

export default PredictionForm;
