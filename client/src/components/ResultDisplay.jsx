function ResultDisplay({ result, onReset }) {
  if (!result) return null;

  const { prediction, probability, confidence } = result;
  const hasDiabetes = prediction === 1;
  const probabilityPercent = (probability * 100).toFixed(1);
  const confidencePercent = (confidence * 100).toFixed(1);

  return (
    <div className={`result-display ${hasDiabetes ? 'diabetes' : 'no-diabetes'}`}>
      <div className="result-icon">
        {hasDiabetes ? '⚠️' : '✓'}
      </div>
      <h2 className="result-title">
        {hasDiabetes ? 'High Risk of Diabetes' : 'Low Risk of Diabetes'}
      </h2>
      
      <div className="result-details">
        <div className="probability-section">
          <div className="probability-label">Prediction Probability</div>
          <div className="probability-value">{probabilityPercent}%</div>
          <div className="probability-bar">
            <div 
              className="probability-fill"
              style={{ width: `${probabilityPercent}%` }}
            />
          </div>
        </div>

        <div className="confidence-section">
          <div className="confidence-label">Confidence Level</div>
          <div className="confidence-value">{confidencePercent}%</div>
        </div>
      </div>

      <div className="result-message">
        {hasDiabetes ? (
          <p>
            Based on the provided health metrics, there is a <strong>{probabilityPercent}%</strong> probability 
            of diabetes. It is recommended to consult with a healthcare professional for further evaluation.
          </p>
        ) : (
          <p>
            Based on the provided health metrics, there is a <strong>{probabilityPercent}%</strong> probability 
            of diabetes. However, regular health check-ups are still recommended.
          </p>
        )}
      </div>

      <div className="disclaimer">
        <strong>Disclaimer:</strong> This prediction is for educational purposes only and should not 
        replace professional medical advice, diagnosis, or treatment. Always consult with qualified 
        healthcare providers for medical concerns.
      </div>

      <button onClick={onReset} className="reset-button">
        Make Another Prediction
      </button>
    </div>
  );
}

export default ResultDisplay;

