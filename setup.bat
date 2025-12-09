@echo off
REM Setup script for Flask User Login & Registration App (Windows PowerShell)
REM This script creates a virtual environment and installs all dependencies

echo ========================================
echo Flask User Login  & Registration App
echo Setup Script (Windows PowerShell)
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org
    exit /b 1
)

echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    exit /b 1
)

echo.
echo Activating virtual environment...
call .\.venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To activate the virtual environment, run:
echo   .\.venv\Scripts\activate.bat
echo.
echo To start the Flask app, run:
echo   python app.py
echo.
echo To run tests, run:
echo   pytest -v
echo.
