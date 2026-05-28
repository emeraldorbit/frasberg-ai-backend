#!/bin/bash

# =============================================================================
# FRASBERG AI Activation Script v6.0.0
# =============================================================================
# This script activates and verifies the Frasberg AI Backend system
# =============================================================================

set -e

echo "🚀 Activating Frasberg AI Backend..."
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "Please create it from .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

echo -e "${GREEN}✅ Environment file found${NC}"
echo ""

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Verify required Frasberg variables
echo "🔍 Verifying Frasberg Model Configuration..."
echo ""

if [ -z "$FRASBERG_MODEL_ENDPOINT" ]; then
    echo -e "${RED}❌ FRASBERG_MODEL_ENDPOINT not set${NC}"
    exit 1
else
    echo -e "${GREEN}✅ FRASBERG_MODEL_ENDPOINT: $FRASBERG_MODEL_ENDPOINT${NC}"
fi

if [ -z "$FRASBERG_MODEL_API_KEY" ]; then
    echo -e "${RED}❌ FRASBERG_MODEL_API_KEY not set${NC}"
    exit 1
else
    echo -e "${GREEN}✅ FRASBERG_MODEL_API_KEY: ${FRASBERG_MODEL_API_KEY:0:20}...${NC}"
fi

if [ -z "$MODEL_ENDPOINT" ]; then
    echo -e "${YELLOW}⚠️  MODEL_ENDPOINT not set${NC}"
else
    echo -e "${GREEN}✅ MODEL_ENDPOINT: $MODEL_ENDPOINT${NC}"
fi

if [ -z "$MODEL_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  MODEL_API_KEY not set${NC}"
else
    echo -e "${GREEN}✅ MODEL_API_KEY: ${MODEL_API_KEY:0:20}...${NC}"
fi

echo ""
echo "🔍 Verifying Project Configuration..."
echo ""

if [ -z "$PROJECT_URL" ]; then
    echo -e "${YELLOW}⚠️  PROJECT_URL not set${NC}"
else
    echo -e "${GREEN}✅ PROJECT_URL: $PROJECT_URL${NC}"
fi

if [ -z "$SERVICE_ROLE_KEY" ]; then
    echo -e "${YELLOW}⚠️  SERVICE_ROLE_KEY not set${NC}"
else
    echo -e "${GREEN}✅ SERVICE_ROLE_KEY: ${SERVICE_ROLE_KEY:0:20}...${NC}"
fi

echo ""
echo "🔍 Verifying GitHub Integration (Optional)..."
echo ""

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  GITHUB_TOKEN not set (optional)${NC}"
else
    echo -e "${GREEN}✅ GITHUB_TOKEN: ${GITHUB_TOKEN:0:15}...${NC}"
fi

if [ -z "$GITHUB_REPO_URL" ]; then
    echo -e "${YELLOW}⚠️  GITHUB_REPO_URL not set (optional)${NC}"
else
    echo -e "${GREEN}✅ GITHUB_REPO_URL: $GITHUB_REPO_URL${NC}"
fi

echo ""
echo -e "${GREEN}✅ Frasberg AI Backend is configured and ready!${NC}"
echo ""
echo "Next steps:"
echo "  1. Start Docker services: docker-compose up -d"
echo "  2. Check API health: curl http://localhost:8000/health"
echo "  3. Access API docs: http://localhost:8000/docs"
echo ""
