import React, { useEffect, useState } from "react";
import "./Recommendations.css";
import { GoogleGenerativeAI } from "@google/generative-ai";

const Recommendations = ({ prediction, formData }) => {
  const [loading, setLoading] = useState(true);
  const [recommendations, setRecommendations] = useState("");

  useEffect(() => {
    if (!prediction) return;

    const fetchRecommendations = async () => {
      try {
        setLoading(true);

        const genAI = new GoogleGenerativeAI("YOUR_API_KEY_HERE");

        const model = genAI.getGenerativeModel({
          model: "gemini-2.0-flash"
        });

        const prompt = `
        You are an AI Career Advisor. Based on the following student's attributes, 
        generate highly personalized, actionable, detailed career recommendations.
        
        Student Details:
        Name: ${formData.name}
        Gender: ${formData.gender}
        Age: ${formData.age}
        CGPA: ${formData.cgpa}
        Matric %: ${formData.matric}
        Intermediate %: ${formData.inter}
        DSA Marks: ${formData.dsa_marks}
        DBMS Marks: ${formData.dbms_marks}
        Backlogs: ${formData.backlogs}
        Reappears: ${formData.reappears}
        History: ${formData.history}
        Programming Proficiency: ${formData.programming}
        GitHub Repos: ${formData.github_repos}
        GitHub Commits/Month: ${formData.github_commits}
        Frameworks: ${formData.frameworks}
        English Level: ${formData.english}
        Coding Hours/Week: ${formData.coding_hours}
        Aptitude Score: ${formData.aptitude}
        Attendance: ${formData.attendance}

        ML Model Prediction: ${prediction.prediction}

        Now generate:
        - Best 3–5 career paths for the student  
        - Reason for each recommendation  
        - Skills to improve  
        - Tools/tech to learn  
        - Extra tips: internships, GitHub improvements, placement advice
        Make the answer crisp, structured, and friendly.
        `;

        const result = await model.generateContent(prompt);
        const text = result.response.text();

        setRecommendations(text);
      } catch (error) {
        console.error("Gemini Recommendation Error:", error);
        setRecommendations("Unable to generate recommendations at this time.");
      }
      setLoading(false);
    };

    fetchRecommendations();
  }, [prediction, formData]);

  return (
    <div className="recommendations-container">
      <h2>💡 AI-Powered Career Recommendations</h2>

      {loading ? (
        <div className="loader">Generating smart recommendations…</div>
      ) : (
        <div className="recommendations-box">
          {recommendations
            .split("\n")
            .filter((line) => line.trim() !== "")
            .map((line, idx) => (
              <p key={idx}>{line}</p>
            ))}
        </div>
      )}
    </div>
  );
};

export default Recommendations;
