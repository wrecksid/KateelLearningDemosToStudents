#!/bin/bash

# Portfolio Optimization - Linux Virtual Environment Setup
echo "Setting up Portfolio Optimization environment for Linux..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete! To activate the environment, run:"
echo "source venv/bin/activate"
echo ""
echo "To run the portfolio optimizer:"
echo "python portfolio_optimizer.py"
# To deactivate the environment, simply run:
echo "deactivate"
echo "You can deactivate the virtual environment by running 'deactivate'."  