#!/usr/bin/env bash
# Script to export OpenAPI to a file

set -e

timeout 5s bash -c '
  uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 &
  server_pid=$!
  sleep 3
  curl http://localhost:8000/openapi.json > openapi.json
  wait $server_pid
'
