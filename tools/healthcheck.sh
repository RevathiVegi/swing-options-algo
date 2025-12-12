#!/usr/bin/env bash
# returns 0 if process running and log file recently updated
pgrep -f simulator.py >/dev/null 2>&1 || exit 1
[ -f /app/logs/sim.log ] || exit 1
# check sim.log updated in last 120s
find /app/logs/sim.log -mmin -2 >/dev/null 2>&1 || exit 1
exit 0
