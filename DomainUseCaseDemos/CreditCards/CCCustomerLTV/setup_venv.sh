#!/bin/bash

# Credit Card CLV Analysis - Virtual Environment Setup (Linux/macOS)
# Author: AI Assistant for Financial Analytics Course
# Date: July 2025

echo "🚀 Setting up Python Virtual Environment for Credit Card CLV Analysis..."
echo "=================================================================="

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
MIN_VERSION="3.8"

if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo "❌ Error: Python 3.8 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv clv_env

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created successfully"

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source clv_env/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing required packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install requirements"
        exit 1
    fi
    echo "✅ All packages installed successfully"
else
    echo "⚠️ Warning: requirements.txt not found. Installing core packages..."
    pip install pandas numpy matplotlib seaborn scikit-learn faker
fi

# Verify installation
echo "🔍 Verifying installation..."
python -c "import pandas, numpy, matplotlib, seaborn, sklearn, faker; print('✅ All core packages imported successfully')"

if [ $? -ne 0 ]; then
    echo "❌ Error: Package verification failed"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "=================================================================="
echo "To use the environment:"
echo "  1. Activate: source clv_env/bin/activate"
echo "  2. Run analysis: python clv_analysis.py"
echo "  3. Generate data: python generate_synthetic_data.py"
echo "  4. Deactivate when done: deactivate"
echo ""
echo "📁 Files in this directory:"
ls -la *.py *.txt *.md 2>/dev/null || echo "No Python files found. Please ensure you have the required .py files."
echo ""
echo "🚀 You're ready to start the CLV analysis!"
