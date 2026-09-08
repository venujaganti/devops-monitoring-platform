#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

if [ ! -f ".env" ]; then
    echo "ERROR: .env does not exist."
    echo "Run ./scripts/setup.sh first."
    exit 1
fi

echo "Starting DevOps Monitoring Platform..."

podman compose up -d --build

echo
echo "Containers:"
podman compose ps

echo
echo "Application started."
echo "Frontend: http://localhost"
echo "Backend:  http://localhost:8000"
echo "Swagger:  http://localhost:8000/docs"