#!/usr/bin/env pwsh
# Test runner script for Flask User Login & Registration App (Windows PowerShell)
# This script runs all pytest tests with proper reporting

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Flask User Login & Registration App" -ForegroundColor Cyan
Write-Host "Test Runner (Windows PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first to create the virtual environment"
    exit 1
}

if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

Write-Host "Running all tests..." -ForegroundColor Yellow
Write-Host ""

# Run pytest with verbose output
& pytest test_app.py -v --tb=short

$testExitCode = $LASTEXITCODE

Write-Host ""
if ($testExitCode -eq 0) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "All tests passed!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Some tests failed (exit code: $testExitCode)" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

exit $testExitCode
