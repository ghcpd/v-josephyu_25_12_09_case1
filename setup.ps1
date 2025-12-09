# PowerShell setup script
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\pip.exe install -r requirements.txt

echo "Virtual environment created and dependencies installed."