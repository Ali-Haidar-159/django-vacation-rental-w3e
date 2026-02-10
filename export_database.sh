#!/bin/bash

# Database export script for vacation_rental project
# This will create a backup of your PostgreSQL database

echo "Exporting database..."

# Export database dump
docker exec postgres-vacation pg_dump -U postgres pythondb > database_backup.sql

echo "Database exported to database_backup.sql"
echo "Add this file to your GitHub repository"