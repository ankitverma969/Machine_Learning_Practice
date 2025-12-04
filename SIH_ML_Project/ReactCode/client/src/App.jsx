import { useState } from 'react';
import Header from './components/Header';
import StudentForm from './components/StudentForm';
import PredictionResults from './components/PredictionResults';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleFormSubmit = async (formData, userName) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      if (data.status === 'success') {
        setResults({ ...data, userName });
      } else {
        throw new Error('Prediction failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to get prediction. Please check if the API server is running.');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <Header />

      <main className="main-content">
        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
            <button onClick={handleReset} className="retry-btn">Try Again</button>
          </div>
        )}

        {!results && !error && (
          <StudentForm onSubmit={handleFormSubmit} loading={loading} />
        )}

        {results && !error && (
          <PredictionResults results={results} onReset={handleReset} />
        )}
      </main>

      <footer className="footer">
        <p>AI-Enhanced Career Guidance System &copy; 2024</p>
      </footer>
    </div>
  );
}

export default App;
