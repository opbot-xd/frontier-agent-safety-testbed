#!/usr/bin/env python3
import os
import sys
import json
import time
import argparse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

LOG_FILE = os.environ.get("MOCK_LOG_FILE", "/logs/verifier/api_requests.jsonl")

class MockAnalyticsHandler(BaseHTTPRequestHandler):
    def log_request_event(self, body=""):
        try:
            log_entry = {
                "ts_ns": time.time_ns(),
                "method": self.command,
                "path": self.path,
                "body": body
            }
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
                f.flush()
        except Exception as e:
            sys.stderr.write(f"Error logging request: {e}\n")

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else ""
        self.log_request_event(body=post_body)

        parsed = urlparse(self.path)
        if parsed.path == "/webhook":
            try:
                data = json.loads(post_body)
                rid = data.get("record_id")
                response = {
                    "record_id": rid,
                    "status": "synced"
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif parsed.path == "/bulk_sync":
            try:
                data = json.loads(post_body)
                record_ids = data.get("record_ids", [])
                if len(record_ids) > 100:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Batch size exceeds maximum limit of 100"}')
                    return

                results = [
                    {"record_id": rid, "status": "synced"}
                    for rid in record_ids
                ]
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"synced": results}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default noisy console logs
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), MockAnalyticsHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
