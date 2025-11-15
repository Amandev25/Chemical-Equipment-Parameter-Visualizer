#!/bin/bash

echo "========================================"
echo "Chemical Equipment Visualizer - Backend Setup"
echo "========================================"
echo ""

echo "[1/6] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/6] Activating virtual environment..."
source venv/bin/activate

echo "[3/6] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/6] Creating migrations..."
python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create migrations"
    exit 1
fi

echo "[5/6] Running migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run migrations"
    exit 1
fi

echo "[6/6] Creating superuser (optional)..."
echo ""
echo "You can skip this step and create superuser later with: python manage.py createsuperuser"
read -p "Create superuser now? (y/n): " create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

echo ""
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To start the development server:"
echo "  python manage.py runserver"
echo ""
echo "API Documentation will be available at:"
echo "  http://localhost:8000/swagger/"
echo ""
echo "Admin Panel:"
echo "  http://localhost:8000/admin/"
echo ""

