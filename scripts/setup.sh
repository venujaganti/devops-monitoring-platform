#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

echo "=========================================="
echo " DevOps Monitoring Platform Setup"
echo "=========================================="

if ! command -v podman >/dev/null 2>&1; then
    echo "ERROR: Podman is not installed."
    exit 1
fi

echo "Podman:"
podman --version

if ! podman compose version >/dev/null 2>&1; then
    echo "ERROR: 'podman compose' is not available."
    exit 1
fi

echo "Podman Compose:"
podman compose version

if [ ! -f ".env" ]; then
    cp ".env.example" ".env"
    echo ".env created."
else
    echo ".env already exists."
fi

echo
echo "Setup completed successfully."
echo
echo "Next command:"
echo "  ./scripts/start.sh"