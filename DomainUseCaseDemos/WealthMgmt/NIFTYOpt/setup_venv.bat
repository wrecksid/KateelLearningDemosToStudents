@echo off
REM Portfolio Optimization - Windows Virtual Environment Setup
echo Setting up Portfolio Optimization environment for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

echo Setup complete! To activate the environment, run:
echo venv\Scripts\activate.bat
echo.
echo To run the portfolio optimizer:
echo python portfolio_optimizer.py
pause
