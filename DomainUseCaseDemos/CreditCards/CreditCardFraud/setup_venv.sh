#!/bin/bash

# Credit Card Fraud Detection - Virtual Environment Setup (Linux/Mac)
# This script creates and activates a Python virtual environment

echo "=== Credit Card Fraud Detection Demo Setup ==="
echo "Setting up Python virtual environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv fraud_detection_env

# Activate virtual environment
echo "Activating virtual environment..."
source fraud_detection_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt

echo "=== Setup Complete ==="
echo "To activate the environment in future sessions, run:"
echo "source fraud_detection_env/bin/activate"
echo ""
echo "To deactivate when done, run:"
echo "deactivate"
echo ""
echo "You can now run the demo scripts:"
echo "python generate_synthetic_data.py"
echo "python credit_card_fraud_detection.py"
