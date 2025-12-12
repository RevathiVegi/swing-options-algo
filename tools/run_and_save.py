#!/usr/bin/env python3
import subprocess, sys, json, datetime, os, re, ast

ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
lines = []

proc = subprocess.Popen([sys.executable, "simulator.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for L in proc.stdout:
    sys.stdout.write(L)
    lines.append(L.rstrip("\n"))
proc.wait()

# append raw run to /app/logs/sim.log
try:
    os.makedirs("/app/logs", exist_ok=True)
    with open("/app/logs/sim.log", "a", encoding="utf-8") as f:
        for L in lines:
            f.write(L + "\n")
except Exception:
    pass

# try to find the Simulation summary dict in the output
summary_obj = None
pattern = re.compile(r"Simulation summary:\s*(\{.*\})")
for L in reversed(lines):
    m = pattern.search(L)
    if m:
        try:
            summary_obj = ast.literal_eval(m.group(1))
        except Exception:
            summary_obj = None
        break

out = {"timestamp": ts, "raw_lines": lines}
if summary_obj and isinstance(summary_obj, dict):
    out["summary"] = summary_obj

# write structured JSON to /app/out
try:
    os.makedirs("/app/out", exist_ok=True)
    path = f"/app/out/summary_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
except Exception:
    pass

sys.exit(proc.returncode or 0)
