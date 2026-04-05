@echo off
REM Portfolio Optimization - Virtual Environment Setup Script (Windows)
REM Author: AI Assistant for Financial Analytics Course
REM Date: July 2025

echo 🚀 Setting up Python virtual environment for Portfolio Optimization...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python version %python_version% detected

REM Create virtual environment
echo 📦 Creating virtual environment 'portfolio_env'...
python -m venv portfolio_env

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call portfolio_env\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing required packages...
if exist requirements.txt (
    pip install -r requirements.txt
    echo ✅ All packages installed successfully!
) else (
    echo ⚠️ requirements.txt not found. Installing basic packages...
    pip install pandas numpy matplotlib seaborn scipy faker jupyter notebook
)

echo.
echo 🎉 Virtual environment setup complete!
echo.
echo To activate the environment in the future, run:
echo    portfolio_env\Scripts\activate.bat
echo.
echo To deactivate the environment, run:
echo    deactivate
echo.
echo To run the demos:
echo    1. Generate synthetic data: python generate_synthetic_data.py
echo    2. Run portfolio optimization: python portfolio_optimization_demo.py
echo    3. Start Jupyter notebook: jupyter notebook

pause
