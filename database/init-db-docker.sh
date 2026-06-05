#!/bin/bash
# This script runs inside PostgreSQL container to initialize the schema

set -e

# Run the schema.sql file
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /schema.sql

echo "✅ Database schema initialized successfully!"
