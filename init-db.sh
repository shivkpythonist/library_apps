#!/bin/bash

# Database initialization script
# This script loads the schema.sql file into PostgreSQL

set -e  # Exit on error

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default values if not set
POSTGRES_USER=${POSTGRES_USER:-library_user}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-library_password}
POSTGRES_HOST=${POSTGRES_HOST:-localhost}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

# Color output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔧 Initializing Database Schema...${NC}"

# Check if schema.sql exists
if [ ! -f "database/schema.sql" ]; then
    echo -e "${RED}❌ Error: database/schema.sql not found${NC}"
    exit 1
fi

# Check if psql is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ Error: psql is not installed. Please install PostgreSQL client.${NC}"
    exit 1
fi

# Load schema into PostgreSQL
echo -e "${YELLOW}Loading schema from database/schema.sql...${NC}"

PGPASSWORD=$POSTGRES_PASSWORD psql \
    -h $POSTGRES_HOST \
    -p $POSTGRES_PORT \
    -U $POSTGRES_USER \
    -f database/schema.sql

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database schema loaded successfully!${NC}"
else
    echo -e "${RED}❌ Error loading database schema${NC}"
    exit 1
fi

# Verify tables were created
echo -e "${YELLOW}Verifying tables...${NC}"

PGPASSWORD=$POSTGRES_PASSWORD psql \
    -h $POSTGRES_HOST \
    -p $POSTGRES_PORT \
    -U $POSTGRES_USER \
    -d library_db \
    -c "\dt"

echo -e "${GREEN}✅ Database initialization complete!${NC}"
