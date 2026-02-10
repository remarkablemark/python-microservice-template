#!/usr/bin/env bash
# Script to test logging

set -e

timeout 3 uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 2>&1 || true
