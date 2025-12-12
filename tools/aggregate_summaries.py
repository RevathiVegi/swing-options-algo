#!/usr/bin/env python3
import json, pathlib, csv
p = pathlib.Path("out")
files = sorted(p.glob("summary_*.json"))
rows = []
for f in files:
    j = json.loads(f.read_text(encoding="utf-8"))
    ts = j.get("timestamp")
    s = j.get("summary", {})
    rows.append({
        "file": f.name,
        "timestamp": ts,
        "count_open": s.get("count_open"),
        "count_closed": s.get("count_closed"),
        "total_realized": s.get("total_realized"),
        "total_fees": s.get("total_fees"),
        "net": s.get("net")
    })
out_csv = p / "summaries.csv"
with out_csv.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=["file","timestamp","count_open","count_closed","total_realized","total_fees","net"])
    writer.writeheader()
    writer.writerows(rows)
print("Wrote", out_csv)
