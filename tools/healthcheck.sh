#!/bin/sh
# returns 0 if sim.log updated within last 120s
if [ -f /app/logs/sim.log ]; then
  [ "$(stat -c %Y /app/logs/sim.log)" -ge $(( $(date +%s) - 120 )) ] && exit 0
fi
exit 1
