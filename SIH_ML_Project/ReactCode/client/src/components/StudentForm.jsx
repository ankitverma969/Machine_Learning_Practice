import { useState } from 'react';
import '../styles/StudentForm.css';

function StudentForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    Name: '',
    Gender: '',
    Age: '',
    CGPA: '',
    Matriculation_Percentage: '',
    Intermediate_Percentage: '',
    Data_Structures_And_Algorithm_Marks: '',
    DBMS_Marks: '',
    Number_of_backlogs: '',
    Number_of_Reappears: '',
    History_of_Reappears_Backlogs: '',
    Programming_proficiency: '',
    GitHub_total_repositories: '',
    GitHub_commits_per_month: '',
    Experience_with_frameworks: '',
    English_proficiency: '',
    Coding_practice_hours_per_week: '',
    Aptitude_score: '',
    Attandance: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const apiData = {
      Gender: formData.Gender,
      Age: parseInt(formData.Age),
      CGPA: parseFloat(formData.CGPA),
      Matriculation_Percentage: parseFloat(formData.Matriculation_Percentage),
      Intermediate_Percentage: parseFloat(formData.Intermediate_Percentage),
      Data_Structures_And_Algorithm_Marks: parseFloat(formData.Data_Structures_And_Algorithm_Marks),
      DBMS_Marks: parseFloat(formData.DBMS_Marks),
      Number_of_backlogs: parseInt(formData.Number_of_backlogs),
      Number_of_Reappears: parseInt(formData.Number_of_Reappears),
      History_of_Reappears_Backlogs: formData.History_of_Reappears_Backlogs,
      Programming_proficiency: formData.Programming_proficiency,
      GitHub_total_repositories: parseInt(formData.GitHub_total_repositories),
      GitHub_commits_per_month: parseInt(formData.GitHub_commits_per_month),
      Experience_with_frameworks: formData.Experience_with_frameworks,
      English_proficiency: formData.English_proficiency,
      Coding_practice_hours_per_week: parseFloat(formData.Coding_practice_hours_per_week),
      Aptitude_score: parseFloat(formData.Aptitude_score),
      Attandance: parseFloat(formData.Attandance)
    };

    onSubmit(apiData, formData.Name);
  };

  return (
    <form className="student-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <h3 className="section-title">Personal Information</h3>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="Name">Full Name</label>
            <input
              type="text"
              id="Name"
              name="Name"
              value={formData.Name}
              onChange={handleChange}
              placeholder="Enter your full name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="Gender">Gender</label>
            <select
              id="Gender"
              name="Gender"
              value={formData.Gender}
              onChange={handleChange}
              required
            >
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="Age">Age</label>
            <input
              type="number"
              id="Age"
              name="Age"
              value={formData.Age}
              onChange={handleChange}
              min="17"
              max="30"
              required
            />
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3 className="section-title">Academic Performance</h3>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="CGPA">CGPA (0-10)</label>
            <input
              type="number"
              id="CGPA"
              name="CGPA"
              value={formData.CGPA}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="10"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="Matriculation_Percentage">Matriculation %</label>
            <input
              type="number"
              id="Matriculation_Percentage"
              name="Matriculation_Percentage"
              value={formData.Matriculation_Percentage}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="100"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="Intermediate_Percentage">Intermediate %</label>
            <input
              type="number"
              id="Intermediate_Percentage"
              name="Intermediate_Percentage"
              value={formData.Intermediate_Percentage}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="100"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="Attandance">Attendance %</label>
            <input
              type="number"
              id="Attandance"
              name="Attandance"
              value={formData.Attandance}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="100"
              required
            />
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3 className="section-title">Subject Marks</h3>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="Data_Structures_And_Algorithm_Marks">DSA Marks (0-100)</label>
            <input
              type="number"
              id="Data_Structures_And_Algorithm_Marks"
              name="Data_Structures_And_Algorithm_Marks"
              value={formData.Data_Structures_And_Algorithm_Marks}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="100"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="DBMS_Marks">DBMS Marks (0-100)</label>
            <input
              type="number"
              id="DBMS_Marks"
              name="DBMS_Marks"
              value={formData.DBMS_Marks}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="100"
              required
            />
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3 className="section-title">Academic History</h3>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="Number_of_backlogs">Number of Backlogs</label>
            <input
              type="number"
              id="Number_of_backlogs"
              name="Number_of_backlogs"
              value={formData.Number_of_backlogs}
              onChange={handleChange}
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="Number_of_Reappears">Number of Reappears</label>
            <input
              type="number"
              id="Number_of_Reappears"
              name="Number_of_Reappears"
              value={formData.Number_of_Reappears}
              onChange={handleChange}
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="History_of_Reappears_Backlogs">History of Reappears/Backlogs</label>
            <input
              type="text"
              id="History_of_Reappears_Backlogs"
              name="History_of_Reappears_Backlogs"
              value={formData.History_of_Reappears_Backlogs}
              onChange={handleChange}
              placeholder="Enter Yes or No"
              required
            />
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3 className="section-title">Technical Skills & GitHub Activity</h3>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="Programming_proficiency">Programming Proficiency</label>
            <select
              id="Programming_proficiency"
              name="Programming_proficiency"
              value={formData.Programming_proficiency}
              onChange={handleChange}
              required
            >
              <option value="">Select Level</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
              <option value="Expert">Expert</option>
            </select>
          </div>

          <div className="form-group">
  <label htmlFor="Experience_with_frameworks">Experience with Frameworks</label>
  <input
    type="text"
    id="Experience_with_frameworks"
    name="Experience_with_frameworks"
    value={formData.Experience_with_frameworks}
    onChange={handleChange}
    placeholder="e.g. React, Django, Node.js, Flutter"
    required
  />
</div>


          <div className="form-group">
            <label htmlFor="GitHub_total_repositories">GitHub Total Repositories</label>
            <input
              type="number"
              id="GitHub_total_repositories"
              name="GitHub_total_repositories"
              value={formData.GitHub_total_repositories}
              onChange={handleChange}
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="GitHub_commits_per_month">GitHub Commits/Month</label>
            <input
              type="number"
              id="GitHub_commits_per_month"
              name="GitHub_commits_per_month"
              value={formData.GitHub_commits_per_month}
              onChange={handleChange}
              min="0"
              required
            />
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3 className="section-title">Additional Skills & Practice</h3>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="English_proficiency">English Proficiency</label>
            <select
              id="English_proficiency"
              name="English_proficiency"
              value={formData.English_proficiency}
              onChange={handleChange}
              required
            >
              <option value="">Select Level</option>
              <option value="Poor">Poor</option>
              <option value="Fair">Fair</option>
              <option value="Good">Good</option>
              <option value="Excellent">Excellent</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="Coding_practice_hours_per_week">Coding Practice (hrs/week)</label>
            <input
              type="number"
              id="Coding_practice_hours_per_week"
              name="Coding_practice_hours_per_week"
              value={formData.Coding_practice_hours_per_week}
              onChange={handleChange}
              step="0.5"
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="Aptitude_score">Aptitude Score (0-100)</label>
            <input
              type="number"
              id="Aptitude_score"
              name="Aptitude_score"
              value={formData.Aptitude_score}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="100"
              required
            />
          </div>
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? 'Analyzing...' : 'Get Career Guidance'}
        </button>
      </div>
    </form>
  );
}

export default StudentForm;
