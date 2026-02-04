# Run tests script for Windows PowerShell

# Activate virtual environment (assuming it's created)
.\.venv\Scripts\Activate.ps1

# Run tests
python -m pytest

Write-Host "Tests completed."