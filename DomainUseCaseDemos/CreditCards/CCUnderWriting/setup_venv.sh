#!/bin/bash

# Credit Card Underwriting Demo - Linux Virtual Environment Setup
# This script creates and configures a Python virtual environment for the demo

echo "=================================================="
echo "Credit Card Underwriting Demo - Environment Setup"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Detected Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv_ccunderwriting

# Check if virtual environment was created successfully
if [ ! -d "venv_ccunderwriting" ]; then
    echo "Error: Failed to create virtual environment."
    exit 1
fi

echo "Virtual environment created successfully."

# Activate virtual environment
echo "Activating virtual environment..."
source venv_ccunderwriting/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing required packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "All packages installed successfully."
    else
        echo "Error: Failed to install some packages. Check requirements.txt"
        exit 1
    fi
else
    echo "Warning: requirements.txt not found. Installing packages manually..."
    pip install faker pandas numpy matplotlib seaborn scikit-learn jupyter jupyterlab
fi

# Create activation script
cat > activate_env.sh << 'EOF'
#!/bin/bash
echo "Activating Credit Card Underwriting Demo environment..."
source venv_ccunderwriting/bin/activate
echo "Environment activated. You can now run:"
echo "  python generate_synthetic_data.py"
echo "  python credit_card_underwriting_demo.py --demo"
echo "  jupyter lab"
EOF

chmod +x activate_env.sh

echo ""
echo "=================================================="
echo "Setup completed successfully!"
echo "=================================================="
echo ""
echo "To activate the environment, run:"
echo "  source venv_ccunderwriting/bin/activate"
echo ""
echo "Or use the convenience script:"
echo "  ./activate_env.sh"
echo ""
echo "To run the demo:"
echo "  1. Generate data: python generate_synthetic_data.py"
echo "  2. Run demo: python credit_card_underwriting_demo.py --demo"
echo "  3. Start Jupyter: jupyter lab"
echo ""
echo "To deactivate the environment:"
echo "  deactivate"
echo ""
echo "=================================================="
echo "Thank you for using the Credit Card Underwriting Demo setup script!"