#!/bin/bash

# Database import script for vacation_rental project
# This will restore the database from backup

echo "Importing database..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 3

# Import database dump
docker exec -i postgres-vacation psql -U postgres pythondb < database_backup.sql

echo "Database imported successfully!"