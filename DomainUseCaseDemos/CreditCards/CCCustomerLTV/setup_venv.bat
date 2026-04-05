@echo off
REM Credit Card CLV Analysis - Virtual Environment Setup (Windows)
REM Author: AI Assistant for Financial Analytics Course
REM Date: July 2025

echo 🚀 Setting up Python Virtual Environment for Credit Card CLV Analysis...
echo ==================================================================

REM Check if python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv clv_env

if %errorlevel% neq 0 (
    echo ❌ Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created successfully

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call clv_env\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo ❌ Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing required packages...
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Error: Failed to install requirements
        pause
        exit /b 1
    )
    echo ✅ All packages installed successfully
) else (
    echo ⚠️ Warning: requirements.txt not found. Installing core packages...
    pip install pandas numpy matplotlib seaborn scikit-learn faker
)

REM Verify installation
echo 🔍 Verifying installation...
python -c "import pandas, numpy, matplotlib, seaborn, sklearn, faker; print('✅ All core packages imported successfully')"

if %errorlevel% neq 0 (
    echo ❌ Error: Package verification failed
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo ==================================================================
echo To use the environment:
echo   1. Activate: clv_env\Scripts\activate.bat
echo   2. Run analysis: python clv_analysis.py
echo   3. Generate data: python generate_synthetic_data.py
echo   4. Deactivate when done: deactivate
echo.
echo 📁 Files in this directory:
dir *.py *.txt *.md 2>nul
echo.
echo 🚀 You're ready to start the CLV analysis!
pause
