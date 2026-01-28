#!/bin/bash

# Cosmic Canvas - Quick Start Script
# This script activates the virtual environment and starts the Streamlit app

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌌 Starting Cosmic Canvas...${NC}"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python -m venv venv
    
    echo -e "${BLUE}Installing dependencies...${NC}"
    ./venv/bin/pip install -r requirements.txt
fi

# Check if streamlit is installed
if ! ./venv/bin/python -c "import streamlit" 2>/dev/null; then
    echo -e "${BLUE}Installing dependencies...${NC}"
    ./venv/bin/pip install -r requirements.txt
fi

echo -e "${GREEN}✓ Environment ready${NC}"
echo -e "${BLUE}Starting Streamlit application...${NC}"
echo ""

# Run streamlit
./venv/bin/streamlit run app.py
