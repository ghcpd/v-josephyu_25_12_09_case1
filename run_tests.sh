#!/bin/bash
# Run tests script for Linux/Mac

# Activate virtual environment (assuming it's created)
source .venv/bin/activate

# Run tests
python -m pytest

echo "Tests completed."