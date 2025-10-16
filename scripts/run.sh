#!/bin/bash
# Convenience script to run the Polymarket monitor with the virtual environment

# Get the project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/setup.sh
fi

echo "Starting Polymarket Trade Monitor..."
echo "Press Ctrl+C to stop"
echo ""

./venv/bin/python polymarket_monitor.py

