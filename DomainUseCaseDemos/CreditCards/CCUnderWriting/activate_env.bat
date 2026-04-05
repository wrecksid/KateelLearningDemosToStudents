@echo off 
echo Activating Credit Card Underwriting Demo environment... 
call venv_ccunderwriting\Scripts\activate.bat 
echo Environment activated. You can now run: 
echo   python generate_synthetic_data.py 
echo   python credit_card_underwriting_demo.py --demo 
echo   jupyter lab 
