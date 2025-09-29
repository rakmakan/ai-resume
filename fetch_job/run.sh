#!/bin/bash

# Simple run script that handles virtual environment activation

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
    python job_search.py
elif command -v uv &> /dev/null; then
    echo "🚀 Running with uv..."
    uv run python job_search.py
else
    echo "❌ No virtual environment found and uv not available."
    echo "Please run ./setup.sh first"
    exit 1
fi