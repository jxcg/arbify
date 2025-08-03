#!/bin/bash

# A script to set the required environment variables for the database connection.
# DO NOT commit this file with real passwords to a public repository.

echo "Setting database environment variables..."

export DB_NAME="arbifydb"
export DB_USER="arbuser"
export DB_PASSWORD="temp_secure_44"
export DB_HOST="143.47.226.107"
export DB_PORT="5432"

echo "✅ Environment variables are set for this terminal session."