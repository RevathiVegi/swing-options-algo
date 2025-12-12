#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
echo "Starting Swing Options simulation via docker compose..."
docker compose up -d
echo "Done. To view logs: docker compose logs -f swing-sim"
