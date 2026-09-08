#!/usr/bin/env bash

set -euo pipefail

echo "Checking backend..."

curl --fail --silent \
    http://localhost:8000/health

echo

echo "Backend: OK"

echo
echo "Checking frontend..."

curl --fail --silent \
    http://localhost/ \
    >/dev/null

echo "Frontend: OK"

echo
echo "All health checks passed."