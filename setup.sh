#!/usr/bin/env bash
python -m venv .venv
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt

echo "Virtual environment created and dependencies installed."