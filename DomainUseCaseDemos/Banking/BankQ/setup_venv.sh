#!/bin/bash

python3 -m venv bankq_env
source bankq_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Virtual environment 'bankq_env' created and dependencies installed."
