#!/bin/bash
# setup_venv.sh
# Create and activate python virtual environment, then install dependencies

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment created and dependencies installed."
echo "Activate with: source venv/bin/activate"
