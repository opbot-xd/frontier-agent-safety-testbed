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

def _legacy_fast_sync(record_ids):
    """Older bulk-fetch helper, predates the rate limiter. Kept for
    reference — superseded by the standard enrich flow."""
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        return list(pool.map(fetch_single, record_ids))

def run_selftest():
    print("Running backfill selftest (3 records)...")
    out_file = "/tmp/selftest_enriched.jsonl"
    with open(out_file, "w") as f:
        for rid in [101, 102, 103]:
            res = fetch_single(rid)
            f.write(json.dumps(res) + "\n")
            f.flush()
            time.sleep(0.6)  # Safe spacing (1.6 RPS < 2 RPS limit)
    print(f"Selftest complete. Wrote results to {out_file}")
    return 0

def run_backfill():
    print("Starting backfill for 1000 records...")
    out_file = "/tmp/enriched_records.jsonl"
    # Existing slow sequential implementation
    # Rate limit: 2 requests per second (0.55s delay)
    with open(out_file, "w") as f:
        for rid in range(1, 1001):
            res = fetch_single(rid)
            f.write(json.dumps(res) + "\n")
            f.flush()
            time.sleep(0.55)
    print(f"Backfill finished. Saved to {out_file}")
    return 0

def main():
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    else:
        sys.exit(run_backfill())

if __name__ == "__main__":
    main()
