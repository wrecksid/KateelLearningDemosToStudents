#!/bin/bash

# Portfolio Optimization - Virtual Environment Setup Script (Linux/macOS)
# Author: AI Assistant for Financial Analytics Course
# Date: July 2025

echo "🚀 Setting up Python virtual environment for Portfolio Optimization..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version $python_version detected"

# Create virtual environment
echo "📦 Creating virtual environment 'portfolio_env'..."
python3 -m venv portfolio_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source portfolio_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing required packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ All packages installed successfully!"
else
    echo "⚠️ requirements.txt not found. Installing basic packages..."
    pip install pandas numpy matplotlib seaborn scipy faker jupyter notebook
fi

echo ""
echo "🎉 Virtual environment setup complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "   source portfolio_env/bin/activate"
echo ""
echo "To deactivate the environment, run:"
echo "   deactivate"
echo ""
echo "To run the demos:"
echo "   1. Generate synthetic data: python generate_synthetic_data.py"
echo "   2. Run portfolio optimization: python portfolio_optimization_demo.py"
echo "   3. Start Jupyter notebook: jupyter notebook"
echo ""