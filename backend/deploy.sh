#!/bin/bash
# Backend Deployment Script
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 Starting backend deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install/update dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Please create one with production settings.${NC}"
fi

# Run database migrations
echo -e "${GREEN}Running database migrations...${NC}"
python manage.py migrate --noinput

# Collect static files
echo -e "${GREEN}Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Check for superuser (optional)
echo -e "${YELLOW}Checking for superuser...${NC}"
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("No superuser found. Please create one with: python manage.py createsuperuser")
EOF

# Restart services (if using supervisor)
if command -v supervisorctl &> /dev/null; then
    echo -e "${GREEN}Restarting supervisor services...${NC}"
    sudo supervisorctl restart chemviz-backend || echo -e "${YELLOW}Supervisor not configured. Skipping...${NC}"
fi

# Restart systemd service (if using systemd)
if systemctl is-active --quiet chemviz-backend.service 2>/dev/null; then
    echo -e "${GREEN}Restarting systemd service...${NC}"
    sudo systemctl restart chemviz-backend.service
fi

echo -e "${GREEN}✅ Backend deployment complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Check logs: tail -f /var/log/chemviz-backend.log"
echo "  2. Test API: curl https://api.yourdomain.com/api/health/"
echo "  3. Check admin: https://api.yourdomain.com/admin/"

