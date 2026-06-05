@echo off
:: ============================================================
:: PM Product Demo Launcher
:: Author: Professor Vinaya Sathyanarayana
:: ============================================================
:: These demos use ES module imports and local fetch.
:: Browsers BLOCK those requests when opened directly as file://.
:: This script starts a local HTTP server so all demos work correctly.
:: ============================================================

echo.
echo  ====================================================
echo   PM Product Demos -- Local Server Launcher
echo  ====================================================
echo.

:: Check Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found. Please install Python 3.x from:
    echo          https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo  Starting local server on http://localhost:8080 ...
echo  Opening browser...
echo.
echo  Press Ctrl+C in this window to stop the server when done.
echo.

:: Open PM demos hub directly
start "" "http://localhost:8080"

:: Start HTTP server (this blocks until Ctrl+C)
python -m http.server 8080
