#!/bin/bash

# Bank Customer Segmentation - Environment Setup Script
# This script creates a Python virtual environment and installs dependencies

echo "🏦 Setting up Bank Customer Segmentation Environment"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv customer_segmentation_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source customer_segmentation_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "To activate the environment in the future, run:"
echo "source customer_segmentation_env/bin/activate"
echo ""
echo "To run the programs:"
echo "1. Generate data: python generate_bank_data.py"
echo "2. Run segmentation: python customer_segmentation.py"
echo ""
echo "To deactivate the environment, run:"
echo "deactivate"
