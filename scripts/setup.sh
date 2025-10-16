#!/bin/bash
# Setup script for Polymarket Trade Monitor

# Get the project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "======================================"
echo "Polymarket Trade Monitor Setup"
echo "======================================"
echo ""
echo "Working directory: $PROJECT_ROOT"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed"
    echo "Please install pip and try again"
    exit 1
fi

echo "✓ pip found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    if [ $? -eq 0 ]; then
        echo "✓ Virtual environment created"
    else
        echo "Error: Failed to create virtual environment"
        echo "You may need to install python3-venv: sudo apt install python3-venv"
        exit 1
    fi
else
    echo "✓ Virtual environment already exists"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
./venv/bin/pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "Error: Failed to install dependencies"
    exit 1
fi

# Make scripts executable
chmod +x polymarket_monitor.py example_usage.py

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To start monitoring:"
echo "  ./venv/bin/python polymarket_monitor.py"
echo ""
echo "Or use the run script:"
echo "  ./scripts/run.sh"
echo ""
echo "Or activate the virtual environment first:"
echo "  source venv/bin/activate"
echo "  python polymarket_monitor.py"
echo ""
echo "For examples and customization:"
echo "  ./venv/bin/python example_usage.py"
echo ""
echo "Check docs/README.md for more information"
echo ""

