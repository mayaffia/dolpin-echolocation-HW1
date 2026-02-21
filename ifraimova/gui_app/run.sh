#!/bin/bash
# Startup script for Dolphin Echolocation GUI Application

echo "=========================================="
echo "Dolphin Echolocation GUI Application"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip3 install -r requirements.txt --quiet

echo ""
echo "Starting server..."
echo "The application will open at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start the server
cd backend
python3 server.py