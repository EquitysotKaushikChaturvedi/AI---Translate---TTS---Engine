#!/bin/bash

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate venv
# Note: On Windows Git Bash, this path format works.
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install deps
echo "Installing requirements..."
pip install -r requirements.txt

# Load env vars if .env exists
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Run the app
echo "Starting Flask app..."
python app.py
