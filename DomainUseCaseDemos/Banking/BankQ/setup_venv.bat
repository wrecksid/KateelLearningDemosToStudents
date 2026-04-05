@echo off
python -m venv bankq_env
call bankq_env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Virtual environment 'bankq_env' created and dependencies installed.
