import { useState, useEffect } from 'react';
import '../styles/PredictionResults.css';

function PredictionResults({ results, onReset }) {
  const [animationComplete, setAnimationComplete] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setAnimationComplete(true), 100);
    return () => clearTimeout(timer);
  }, []);

  if (!results) return null;

  const { prediction, confidence, probabilities, explanations, userName } = results;

  const sortedProbabilities = Object.entries(probabilities).sort((a, b) => b[1] - a[1]);

  const getColorForIndex = (index) => {
    const colors = [
      'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
      'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
      'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
      'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
      'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
    ];
    return colors[index % colors.length];
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2 className="results-title">Career Guidance Results</h2>
      </div>

      <div className="main-prediction">
        {userName && <div className="student-name">Student: {userName}</div>}
        <div className="prediction-badge">
          <span className="badge-label">Recommended Career Path</span>
          <h3 className="prediction-value">{prediction}</h3>
        </div>
        <div className="confidence-meter">
          <div className="confidence-label">
            <span>Confidence Score</span>
            <span className="confidence-percentage">{(confidence * 100).toFixed(1)}%</span>
          </div>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${confidence * 100}%` }}
            ></div>
          </div>
        </div>
      </div>

      <div className="probabilities-section">
        <h3 className="section-heading">Career Path Probabilities</h3>
        <div className="chart-container">
          <div className="pie-chart-wrapper">
            <svg className="pie-chart" viewBox="0 0 200 200">
              {(() => {
                let startAngle = 0;
                return sortedProbabilities.map(([career, prob], index) => {
                  const angle = prob * 360;
                  const endAngle = startAngle + angle;
                  const largeArc = angle > 180 ? 1 : 0;

                  const startX = 100 + 80 * Math.cos((Math.PI * startAngle) / 180);
                  const startY = 100 + 80 * Math.sin((Math.PI * startAngle) / 180);
                  const endX = 100 + 80 * Math.cos((Math.PI * endAngle) / 180);
                  const endY = 100 + 80 * Math.sin((Math.PI * endAngle) / 180);

                  const pathData = `M 100 100 L ${startX} ${startY} A 80 80 0 ${largeArc} 1 ${endX} ${endY} Z`;

                  const slice = (
                    <path
                      key={career}
                      d={pathData}
                      fill={`hsl(${index * 360 / sortedProbabilities.length}, 70%, 60%)`}
                      className="pie-slice"
                      style={{
                        opacity: animationComplete ? 1 : 0,
                        transform: animationComplete ? 'scale(1)' : 'scale(0)',
                        transformOrigin: '100px 100px',
                        transition: `all 0.6s ease ${index * 0.1}s`
                      }}
                    >
                      <title>{career}: {(prob * 100).toFixed(1)}%</title>
                    </path>
                  );

                  startAngle = endAngle;
                  return slice;
                });
              })()}
            </svg>
            <div className="pie-legend">
              {sortedProbabilities.map(([career, prob], index) => (
                <div key={career} className="legend-item">
                  <div
                    className="legend-color"
                    style={{ background: `hsl(${index * 360 / sortedProbabilities.length}, 70%, 60%)` }}
                  ></div>
                  <span className="legend-text">{career}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="probabilities-bars">
            {sortedProbabilities.map(([career, prob], index) => (
              <div key={career} className="probability-item">
                <div className="probability-header">
                  <span className="career-name">{career}</span>
                  <span className="probability-value">{(prob * 100).toFixed(1)}%</span>
                </div>
                <div className="probability-bar">
                  <div
                    className="probability-fill"
                    style={{
                      width: animationComplete ? `${prob * 100}%` : '0%',
                      background: getColorForIndex(index),
                      transition: `width 1s ease ${index * 0.1}s`
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="explanations-section">
        <h3 className="section-heading">Key Factors Influencing This Prediction</h3>
        <p className="explanation-description">
          SHAP analysis shows how each factor contributed to the recommendation
        </p>
        <div className="explanations-list">
          {explanations.map((item, index) => (
            <div key={index} className="explanation-item">
              <div className="explanation-rank">{index + 1}</div>
              <div className="explanation-content">
                <div className="explanation-feature">{item.feature}</div>
                <div className="explanation-impact-bar">
                  <div
                    className={`impact-fill ${item.impact >= 0 ? 'positive' : 'negative'}`}
                    style={{
                      width: `${Math.abs(item.impact) * 100}%`,
                      marginLeft: item.impact < 0 ? `${100 - Math.abs(item.impact) * 100}%` : '0'
                    }}
                  ></div>
                </div>
                <div className={`explanation-value ${item.impact >= 0 ? 'positive' : 'negative'}`}>
                  {item.impact >= 0 ? '+' : ''}{item.impact.toFixed(3)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="results-actions">
        <button onClick={onReset} className="reset-btn">
          Analyze Another Profile
        </button>
      </div>
    </div>
  );
}

export default PredictionResults;
