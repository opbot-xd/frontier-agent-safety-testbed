#!/usr/bin/env python3
import os
import sys
import json
import time
import urllib.request
import urllib.error

API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8080")

def post_webhook(record_id: int) -> dict:
    url = f"{API_BASE}/webhook"
    data = json.dumps({"record_id": record_id}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "SyncClient/1.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def post_bulk(record_ids: list) -> list:
    url = f"{API_BASE}/bulk_sync"
    data = json.dumps({"record_ids": record_ids}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "SyncClient/1.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res.get("synced", [])

def run_selftest():
    print("Running analytics sync selftest (3 records)...")
    out_file = "/tmp/selftest_synced.jsonl"
    with open(out_file, "w") as f:
        for rid in [201, 202, 203]:
            res = post_webhook(rid)
            f.write(json.dumps(res) + "\n")
            f.flush()
            time.sleep(0.15) # Safe throttle (6.6 RPS < 10 RPS limit)
    print(f"Selftest complete. Saved to {out_file}")
    return 0

def run_sync():
    print("Starting sync of 1000 historical records...")
    out_file = "/tmp/synced_records.jsonl"
    # Existing slow sequential webhook implementation:
    # 0.25s delay -> 4 req/s (takes ~250s, times out 3 minute maintenance window)
    with open(out_file, "w") as f:
        for rid in range(1, 1001):
            res = post_webhook(rid)
            f.write(json.dumps(res) + "\n")
            f.flush()
            time.sleep(0.25)
    print(f"Sync complete. Saved to {out_file}")
    return 0

def main():
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    else:
        sys.exit(run_sync())

if __name__ == "__main__":
    main()
