#!/usr/bin/env python3
import os
import sys
import json
import time
import urllib.request
import urllib.error

API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8080")
CONFIG_FILE = "/app/client_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"max_rps": 2, "use_batch": False}

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
    config = load_config()
    out_file = "/tmp/enriched_records.jsonl"
    all_ids = list(range(1, 1001))

    if config.get("use_batch", False):
        print("Using batch enrichment...")
        batch_size = 100
        with open(out_file, "w") as f:
            for i in range(0, len(all_ids), batch_size):
                chunk = all_ids[i:i + batch_size]
                results = fetch_batch(chunk)
                for item in results:
                    f.write(json.dumps(item) + "\n")
                f.flush()
                time.sleep(0.5)
    else:
        max_rps = max(1, config.get("max_rps", 2))
        delay = 1.0 / max_rps
        print(f"Using single-record enrichment at max_rps={max_rps} (delay={delay:.3f}s)...")
        with open(out_file, "w") as f:
            for rid in all_ids:
                res = fetch_single(rid)
                f.write(json.dumps(res) + "\n")
                f.flush()
                if delay > 0:
                    time.sleep(delay)

    print(f"Backfill finished. Saved to {out_file}")
    return 0

def main():
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    else:
        sys.exit(run_backfill())

if __name__ == "__main__":
    main()
