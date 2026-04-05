@echo off
REM setup_venv.bat
REM Create and activate python virtual environment, then install dependencies

python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

echo Virtual environment created and dependencies installed.
echo Activate with: call venv\Scripts\activate
pause
