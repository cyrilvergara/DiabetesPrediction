# Diabetes Prediction Web App

A full-stack web application that enables users to input health-related data and receive a prediction on whether they are likely to have diabetes, using a binary classification model trained on the Pima Indians Diabetes Dataset.

**COMP377 AI for Software Developers (SEC. 001) Group 1**

## Overview

This application uses an Artificial Neural Network (ANN) built with TensorFlow/Keras to predict diabetes risk based on 8 health metrics. The model was trained on the Pima Indians Diabetes Dataset and achieves approximately 74% accuracy on the test set.

### Features

- **Frontend**: Responsive React SPA with modern UI
- **Backend**: Python Flask API with TensorFlow/Keras model inference
- **Model**: Trained ANN with 3 hidden layers
- **Validation**: Comprehensive input validation on both frontend and backend
- **Deployment**: Ready for deployment on Render.com

## Dataset

The model is trained on the **Pima Indians Diabetes Dataset**, which contains 768 samples with 8 features:

1. **Pregnancies** - Number of times pregnant (0-20)
2. **Glucose** - Plasma glucose concentration (mg/dL, 0-500)
3. **Blood Pressure** - Diastolic blood pressure (mm Hg, 0-200)
4. **Skin Thickness** - Triceps skin fold thickness (mm, 0-100)
5. **Insulin** - 2-Hour serum insulin (mu U/ml, 0-1000)
6. **BMI** - Body mass index (kg/m², 0-100)
7. **Diabetes Pedigree Function** - Diabetes pedigree function (0-5)
8. **Age** - Age in years (0-150)

### Model Performance

- **Accuracy**: 74.03%
- **Precision**: 62.96%
- **Recall**: 62.96%
- **F1-Score**: 62.96%

## Project Structure

```
DiabetesPrediction/
├── backend/
│   ├── app.py                 # Flask application
│   ├── train_model.py         # Model training script
│   ├── requirements.txt       # Python dependencies
│   ├── Procfile              # Render deployment config
│   ├── runtime.txt           # Python version
│   ├── model/
│   │   ├── __init__.py       # Model loading and prediction
│   │   ├── model.h5          # Trained TensorFlow model
│   │   └── scaler.pkl        # Feature scaler
│   └── tests/
│       └── test_app.py        # Backend tests
├── client/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── App.css           # Styles
│   │   └── components/
│   │       ├── PredictionForm.jsx
│   │       └── ResultDisplay.jsx
│   ├── package.json
│   └── vite.config.js
├── render-build.sh           # Build script for Render
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+ (specified in `backend/runtime.txt`)
- Node.js 16+ and npm
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DiabetesPrediction
   ```

2. **Set up Python backend**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # Windows CMD:
   .\.venv\Scripts\activate.bat
   # Linux/Mac:
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r backend/requirements.txt
   ```

3. **Train the model** (if model files don't exist)
   ```bash
   cd backend
   python train_model.py
   ```
   This will download the dataset, train the model, and save `model.h5` and `scaler.pkl` in `backend/model/`.

4. **Set up frontend**
   ```bash
   cd client
   npm install
   ```

## Running the Application

### Development Mode

1. **Start the backend server**
   ```bash
   cd backend
   python app.py
   ```
   Backend runs on `http://localhost:5000`

2. **Start the frontend development server** (in a new terminal)
   ```bash
   cd client
   npm run dev
   ```
   Frontend runs on `http://localhost:5173` (Vite default)

   The Vite dev server is configured to proxy `/predict` requests to the backend.

### Production Build

1. **Build the frontend**
   ```bash
   cd client
   npm run build
   ```
   This creates a `dist` folder with the production build.

2. **Run the backend** (which serves the frontend)
   ```bash
   cd backend
   python app.py
   ```
   The Flask app serves the frontend from `client/dist` and handles API requests.

## API Documentation

### POST /predict

Predicts diabetes risk based on health metrics.

**Request Body:**
```json
{
  "features": {
    "pregnancies": 6,
    "glucose": 148,
    "blood_pressure": 72,
    "skin_thickness": 35,
    "insulin": 0,
    "bmi": 33.6,
    "diabetes_pedigree_function": 0.627,
    "age": 50
  }
}
```

**Response (Success):**
```json
{
  "prediction": 1,
  "probability": 0.8234,
  "confidence": 0.6468
}
```

- `prediction`: Binary prediction (0 = no diabetes, 1 = diabetes)
- `probability`: Model's probability output (0-1)
- `confidence`: Confidence level (0-1)

**Response (Error):**
```json
{
  "error": "missing required features: glucose, bmi"
}
```

## Testing

### Backend Tests

Run the backend tests:
```bash
# PowerShell
$env:PYTHONPATH='backend'; python -m pytest -q backend/tests

# CMD
set PYTHONPATH=backend && python -m pytest -q backend/tests

# Linux/Mac
PYTHONPATH=backend python -m pytest -q backend/tests
```

## Deployment to Render

1. **Create a new Web Service** on Render.com
2. **Connect your repository**
3. **Configure the service:**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. **Set environment variables** (if needed)
5. **Deploy**

The `render-build.sh` script will:
- Build the frontend (`npm run build` in `client/`)
- Install backend dependencies

Make sure the model files (`model.h5` and `scaler.pkl`) are committed to the repository or available in the deployment environment.

## Model Training Details

The model training script (`backend/train_model.py`) performs:

1. **Data Loading**: Downloads Pima Indians Diabetes Dataset
2. **Preprocessing**:
   - Handles missing values (replaces 0s with NaN, then imputes with median)
   - Splits data into train/test sets (80/20)
   - Normalizes features using StandardScaler
3. **Model Architecture**:
   - Input layer: 8 features
   - Hidden layers: 64 → 32 → 16 neurons with ReLU activation
   - Dropout layers (0.3) for regularization
   - Output layer: 1 neuron with sigmoid activation
4. **Training**: 100 epochs with Adam optimizer, binary crossentropy loss
5. **Evaluation**: Calculates accuracy, precision, recall, F1-score
6. **Saving**: Saves model as `model.h5` and scaler as `scaler.pkl`

## Dataset Citation

Pima Indians Diabetes Dataset:
- Source: UCI Machine Learning Repository
- URL: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
- Original source: https://archive.ics.uci.edu/ml/datasets/diabetes

## Disclaimer

**This application is for educational purposes only.** The predictions provided by this model should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.

## License

See LICENSE file for details.

## Contributors

COMP377 AI for Software Developers (SEC. 001) Group 1
