#!/usr/bin/env bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Virtualenv created and dependencies installed. Activate with 'source .venv/bin/activate' (Unix) or '.\\.venv\\Scripts\\Activate.ps1' (Windows PowerShell)."