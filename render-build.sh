#!/usr/bin/env bash
# Exit on error
set -o errexit

# Build Frontend
echo "Building Frontend..."
cd client
npm install
npm run build
cd ..

# Install Backend Dependencies
echo "Installing Backend Dependencies..."
cd backend
pip install -r requirements.txt
