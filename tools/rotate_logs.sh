#!/usr/bin/env bash
LOG=/app/logs/sim.log
[ -f "$LOG" ] || exit 0
MAX=52428800  # 50MB
size=$(stat -c%s "$LOG" 2>/dev/null || echo 0)
if [ "$size" -ge "$MAX" ]; then
  mv "$LOG" "${LOG}.$(date -u +%Y%m%dT%H%M%SZ).old"
  : > "$LOG"
fi
