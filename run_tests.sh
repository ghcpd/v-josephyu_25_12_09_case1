#!/bin/bash
# Test runner script for Flask User Login & Registration App (Linux/macOS Bash)
# This script runs all pytest tests with proper reporting

echo "========================================"
echo "Flask User Login & Registration App"
echo "Test Runner (Linux/macOS Bash)"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found" >&2
    echo "Please run setup.sh first to create the virtual environment" >&2
    exit 1
fi

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..." 
    source .venv/bin/activate
fi

echo "Running all tests..."
echo ""

# Run pytest with verbose output
pytest test_app.py -v --tb=short
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "========================================"
    echo "All tests passed!"
    echo "========================================"
else
    echo "========================================"
    echo "Some tests failed (exit code: $TEST_EXIT_CODE)"
    echo "========================================"
fi

exit $TEST_EXIT_CODE
