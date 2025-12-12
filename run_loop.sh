#!/usr/bin/env bash
set -euo pipefail

# You can tune interval; in prod maybe 30s-60s or schedule by market hours.
INTERVAL=${SIM_RUN_INTERVAL:-60}

while true; do
  echo "$(date -u) - running simulator"
  python simulator.py || echo "simulator exited with $? — continuing"
  sleep "$INTERVAL"
done
