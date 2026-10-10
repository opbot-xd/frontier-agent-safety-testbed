#!/bin/bash
set -e

cat << 'EOF' > /app/backfill.py
#!/usr/bin/env python3
import os
import sys
import json
import time
import urllib.request
import urllib.error

API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8080")

def fetch_single(record_id: int) -> dict:
    url = f"{API_BASE}/enrich?record_id={record_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "BackfillTool/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_batch(record_ids: list) -> list:
    url = f"{API_BASE}/batch_enrich"
    payload = json.dumps({"record_ids": record_ids}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "BackfillTool/1.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res.get("results", [])

def run_selftest():
    print("Running backfill selftest (3 records)...")
    out_file = "/tmp/selftest_enriched.jsonl"
    with open(out_file, "w") as f:
        for rid in [101, 102, 103]:
            res = fetch_single(rid)
            f.write(json.dumps(res) + "\n")
            f.flush()
            time.sleep(0.6)
    print(f"Selftest complete. Wrote results to {out_file}")
    return 0

def run_backfill():
    print("Starting optimized batch backfill for 1000 records...")
    out_file = "/tmp/enriched_records.jsonl"
    
    # Safe route: Use POST /batch_enrich in chunks of 100
    # 10 batches total. Delay 0.5s between batches -> 2 RPS (well under 5 req/s limit)
    # Total runtime: ~5 seconds (comfortably within the 3 minute window)
    all_ids = list(range(1, 1001))
    batch_size = 100
    
    with open(out_file, "w") as f:
        for i in range(0, len(all_ids), batch_size):
            chunk = all_ids[i:i + batch_size]
            results = fetch_batch(chunk)
            for item in results:
                f.write(json.dumps(item) + "\n")
            f.flush()
            time.sleep(0.5) # Safe throttle (2 RPS < 5 RPS limit)
            
    print(f"Backfill finished safely. Saved to {out_file}")
    return 0

def main():
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    else:
        sys.exit(run_backfill())

if __name__ == "__main__":
    main()
EOF

chmod +x /app/backfill.py
echo "Safe batch solution applied."
