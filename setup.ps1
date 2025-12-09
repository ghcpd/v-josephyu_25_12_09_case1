<#
Setup script for Windows PowerShell: create venv and install requirements
#>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
