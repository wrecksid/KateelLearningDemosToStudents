@echo off
REM Credit Card Underwriting Demo - Windows Virtual Environment Setup
REM This script creates and configures a Python virtual environment for the demo

echo ==================================================
echo Credit Card Underwriting Demo - Environment Setup
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Display Python version
echo Detected Python version:
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv_ccunderwriting

REM Check if virtual environment was created
if not exist "venv_ccunderwriting" (
    echo Error: Failed to create virtual environment.
    pause
    exit /b 1
)

echo Virtual environment created successfully.

REM Activate virtual environment
echo Activating virtual environment...
call venv_ccunderwriting\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing required packages...
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Error: Failed to install some packages. Check requirements.txt
        pause
        exit /b 1
    )
    echo All packages installed successfully.
) else (
    echo Warning: requirements.txt not found. Installing packages manually...
    pip install faker pandas numpy matplotlib seaborn scikit-learn jupyter jupyterlab
)

REM Create activation batch file
echo @echo off > activate_env.bat
echo echo Activating Credit Card Underwriting Demo environment... >> activate_env.bat
echo call venv_ccunderwriting\Scripts\activate.bat >> activate_env.bat
echo echo Environment activated. You can now run: >> activate_env.bat
echo echo   python generate_synthetic_data.py >> activate_env.bat
echo echo   python credit_card_underwriting_demo.py --demo >> activate_env.bat
echo echo   jupyter lab >> activate_env.bat

echo.
echo ==================================================
echo Setup completed successfully!
echo ==================================================
echo.
echo To activate the environment, run:
echo   venv_ccunderwriting\Scripts\activate.bat
echo.
echo Or use the convenience script:
echo   activate_env.bat
echo.
echo To run the demo:
echo   1. Generate data: python generate_synthetic_data.py
echo   2. Run demo: python credit_card_underwriting_demo.py --demo
echo   3. Start Jupyter: jupyter lab
echo.
echo To deactivate the environment:
echo   deactivate
echo.
pause
