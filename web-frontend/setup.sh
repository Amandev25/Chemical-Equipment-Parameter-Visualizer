#!/bin/bash

echo "========================================"
echo "Chemical Equipment Visualizer - Frontend Setup"
echo "========================================"
echo ""

echo "[1/2] Installing dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/2] Setup completed!"
echo ""
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To start the development server:"
echo "  npm run dev"
echo ""
echo "The app will be available at:"
echo "  http://localhost:3000"
echo ""
echo "Make sure the backend is running at:"
echo "  http://localhost:8000"
echo ""

