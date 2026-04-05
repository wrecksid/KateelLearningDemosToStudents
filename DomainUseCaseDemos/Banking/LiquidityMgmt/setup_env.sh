#!/bin/bash

# Virtual Environment Setup Script for Liquidity Management Demo
# This script creates a Python virtual environment and installs required dependencies

echo "🏦 Setting up Liquidity Management Monte Carlo Simulation Environment"
echo "=================================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Display Python version
echo "🐍 Python version: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv liquidity_env

# Check if virtual environment was created successfully
if [ ! -d "liquidity_env" ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created successfully"

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source liquidity_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing required packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Requirements installed successfully"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Display installed packages
echo "📋 Installed packages:"
pip list

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To activate the environment, run:"
echo "    source liquidity_env/bin/activate"
echo ""
echo "To deactivate the environment, run:"
echo "    deactivate"
echo ""
echo "To run the data generator:"
echo "    python generate_synthetic_liquidity_data.py --rows 10000"
echo ""
echo "To run the Monte Carlo simulation:"
echo "    python liquidity_monte_carlo_simulation.py --data synthetic_liquidity_data.csv"
