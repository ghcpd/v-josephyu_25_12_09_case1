@echo off
REM Test runner script for Flask User Login & Registration App (Windows Batch)
REM This script runs all pytest tests with proper reporting

echo ========================================
echo Flask User Login & Registration App
echo Test Runner (Windows Batch)
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Virtual environment is not activated
    echo Activating virtual environment...
    call .\.venv\Scripts\activate.bat
    if errorlevel 1 (
        echo Error: Failed to activate virtual environment
        exit /b 1
    )
)

echo Running all tests...
echo.

REM Run pytest with verbose output and coverage
pytest test_app.py -v --tb=short
set TEST_EXIT_CODE=%ERRORLEVEL%

echo.
if %TEST_EXIT_CODE% equ 0 (
    echo ========================================
    echo All tests passed!
    echo ========================================
) else (
    echo ========================================
    echo Some tests failed (exit code: %TEST_EXIT_CODE%)
    echo ========================================
)

exit /b %TEST_EXIT_CODE%
