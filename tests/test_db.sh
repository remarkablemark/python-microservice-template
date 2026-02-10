#!/usr/bin/env bash

# Script to test database functionality

set -e

ROOT_DIR=$(git rev-parse --show-toplevel)
DATABASE_FILE="$ROOT_DIR/test.db"

echo "Setting up test database..."
export DATABASE_URL="sqlite:////$DATABASE_FILE"

echo "Creating initial migration..."
uv run alembic revision --autogenerate -m "Initial migration with User model"

echo "Applying migrations..."
uv run alembic upgrade head

echo "Starting server in background..."
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo "Testing user creation..."
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "is_active": true
  }' && echo

echo "Testing user retrieval..."
curl "http://127.0.0.1:8000/users/1" && echo

echo "Stopping server..."
kill $SERVER_PID

echo "Cleaning up..."
rm -f $DATABASE_FILE
rm -rf $ROOT_DIR/alembic/versions/*

echo "Done!"
