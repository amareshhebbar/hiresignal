#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

csv_path = sys.argv[1] if len(sys.argv) > 1 else "submission.csv"
jsonl_path = sys.argv[2] if len(sys.argv) > 2 else "candidates.jsonl"

with open(csv_path) as f:
    rows = list(csv.DictReader(f))

cands = {}
with open(jsonl_path) as f:
    for line in f:
        c = json.loads(line)
        cands[c["candidate_id"]] = c

print(f"rows: {len(rows)}")
print(f"\ntop 10:")
for r in rows[:10]:
    c = cands.get(r["candidate_id"])
    if c:
        p = c["profile"]
        sig = c["redrob_signals"]
        print(f"  [{r['rank']:3}] {r['candidate_id']}  {p['current_title']:<40}  yoe={p['years_of_experience']:.1f}  rr={sig['recruiter_response_rate']:.2f}  notice={sig['notice_period_days']}d")
        print(f"       {r['reasoning']}")
        print()
