# Diabetes Prediction Backend (skeleton)

This folder contains a minimal Flask backend skeleton to receive requests and run inference.

Quick notes
- HTTP GET / => health/status
- HTTP POST /predict => accepts JSON {"features": {...} } and returns {"prediction": 0|1}

Local dev
1. Create a virtual environment and activate it.
    `python -m venv .venv`
    `.\.venv\Scripts\Activate.ps1`
2. pip install -r requirements.txt
    `pip install -r backend/requirements.txt`
3. python app.py  # runs on http://localhost:5000
    `python backend/app.py`
4. Run tests 
    for cmd
    `set PYTHONPATH=backend && python -m pytest -q backend/tests`
    for PowerShell
    `$env:PYTHONPATH='backend'; python -m pytest -q backend/tests`
    
Deploying to Render
1. Create a new Web Service on Render and connect your repo.
2. Set the root directory to `backend` (so Render uses the `Procfile` and `requirements.txt`).
3. Build command: pip install -r requirements.txt
4. Start command: gunicorn app:app

Replace the model stub in `backend/model/__init__.py` with your real model loading and inference code when ready.
