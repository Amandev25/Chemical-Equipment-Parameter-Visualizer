#!/bin/bash
# Frontend Deployment Script
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 Starting frontend deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    npm install
fi

# Check for .env.production file
if [ ! -f ".env.production" ]; then
    echo -e "${YELLOW}Warning: .env.production file not found.${NC}"
    echo -e "${YELLOW}Creating from .env.example if it exists...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env.production
    fi
fi

# Build production bundle
echo -e "${GREEN}Building production bundle...${NC}"
npm run build

# Check if build was successful
if [ ! -d "dist" ]; then
    echo -e "${RED}❌ Build failed! dist directory not found.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build successful!${NC}"
echo -e "${YELLOW}Build output: dist/${NC}"

# Deployment options
echo -e "${YELLOW}Choose deployment method:${NC}"
echo "  1. Vercel (recommended)"
echo "  2. Netlify"
echo "  3. Manual (copy dist/ to server)"
echo "  4. Skip deployment"

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        if command -v vercel &> /dev/null; then
            echo -e "${GREEN}Deploying to Vercel...${NC}"
            vercel --prod
        else
            echo -e "${RED}Vercel CLI not installed. Install with: npm i -g vercel${NC}"
        fi
        ;;
    2)
        if command -v netlify &> /dev/null; then
            echo -e "${GREEN}Deploying to Netlify...${NC}"
            netlify deploy --prod --dir=dist
        else
            echo -e "${RED}Netlify CLI not installed. Install with: npm i -g netlify-cli${NC}"
        fi
        ;;
    3)
        echo -e "${YELLOW}Manual deployment:${NC}"
        echo "  Copy the 'dist' directory to your web server"
        echo "  Example: scp -r dist/* user@server:/var/www/chemviz-frontend/"
        ;;
    4)
        echo -e "${YELLOW}Skipping deployment.${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice. Skipping deployment.${NC}"
        ;;
esac

echo -e "${GREEN}✅ Frontend deployment script complete!${NC}"

