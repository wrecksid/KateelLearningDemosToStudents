@echo off
REM Credit Card Fraud Detection - Virtual Environment Setup (Windows)
REM This script creates and activates a Python virtual environment

echo === Credit Card Fraud Detection Demo Setup ===
echo Setting up Python virtual environment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv fraud_detection_env

REM Activate virtual environment
echo Activating virtual environment...
call fraud_detection_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt

echo === Setup Complete ===
echo To activate the environment in future sessions, run:
echo fraud_detection_env\Scripts\activate.bat
echo.
echo To deactivate when done, run:
echo deactivate
echo.
echo You can now run the demo scripts:
echo python generate_synthetic_data.py
echo python credit_card_fraud_detection.py
pause
