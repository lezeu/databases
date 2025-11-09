#!/bin/bash
# Initialize PostgreSQL database
set -e

echo "Initializing PostgreSQL database..."

# Wait for PostgreSQL to be ready
until docker exec postgres pg_isready -U postgres > /dev/null 2>&1; do
    echo "Waiting for PostgreSQL..."
    sleep 1
done

# Create database if it doesn't exist
docker exec postgres psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'online_shopping'" | grep -q 1 || \
docker exec postgres psql -U postgres -c "CREATE DATABASE online_shopping"

# Initialize schema
docker exec -i postgres psql -U postgres -d online_shopping < sql/online_shopping_schema.sql

echo "✅ Database initialized"
