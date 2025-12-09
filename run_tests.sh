#!/usr/bin/env bash
# Activate venv if present
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi
pytest -q
