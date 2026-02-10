#!/usr/bin/env bash
# Script to test bearer token authentication

set -e

echo "Starting server with authentication enabled..."
export API_TOKENS="test-token-123,another-token-456"

# Start server in background
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo -e "\n=== Testing without authentication ==="
echo "Should return 401 Unauthorized:"
curl -i http://127.0.0.1:8000/protected/ 2>/dev/null | head -n 1

echo -e "\n=== Testing with invalid token ==="
echo "Should return 403 Forbidden:"
curl -i -H "Authorization: Bearer invalid-token" http://127.0.0.1:8000/protected/ 2>/dev/null | head -n 1

echo -e "\n=== Testing with valid token ==="
echo "Should return 200 OK:"
curl -i -H "Authorization: Bearer test-token-123" http://127.0.0.1:8000/protected/ 2>/dev/null | head -n 1
echo "Response body:"
curl -H "Authorization: Bearer test-token-123" http://127.0.0.1:8000/protected/ && echo

echo -e "\n=== Testing protected data endpoint ==="
echo "Response:"
curl -H "Authorization: Bearer test-token-123" http://127.0.0.1:8000/protected/data && echo

echo -e "\n=== Testing with second valid token ==="
echo "Response:"
curl -H "Authorization: Bearer another-token-456" http://127.0.0.1:8000/protected/ && echo

echo -e "\nStopping server..."
kill $SERVER_PID

echo "Done!"
