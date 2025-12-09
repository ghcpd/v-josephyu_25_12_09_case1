# Setup script for Windows PowerShell

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

Write-Host "Setup complete. Run '.\.venv\Scripts\Activate.ps1' then 'python app.py' to start the app."