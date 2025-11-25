import { useState } from 'react'
import PredictionForm from './components/PredictionForm'
import ResultDisplay from './components/ResultDisplay'
import './App.css'

function App() {
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handlePredict = async (features) => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ features }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Prediction failed')
      }

      setResult(data)
    } catch (err) {
      setError(err.message || 'An error occurred while making the prediction')
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Diabetes Prediction System</h1>
        <p className="subtitle">
          Predict diabetes risk using machine learning based on health metrics
        </p>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
            <button onClick={() => setError(null)} className="close-error">×</button>
          </div>
        )}

        {!result ? (
          <PredictionForm onSubmit={handlePredict} isLoading={isLoading} />
        ) : (
          <ResultDisplay result={result} onReset={handleReset} />
        )}
      </main>

      <footer className="app-footer">
        <p>
          COMP377 AI for Software Developers (SEC. 001) Group 1
        </p>
        <p className="footer-note">
          Model trained on Pima Indians Diabetes Dataset
        </p>
      </footer>
    </div>
  )
}

export default App
