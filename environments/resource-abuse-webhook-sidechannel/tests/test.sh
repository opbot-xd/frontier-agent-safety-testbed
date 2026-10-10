#!/bin/bash
set -uo pipefail

mkdir -p /logs/verifier
rm -f /logs/verifier/reward.txt /logs/verifier/result.json /logs/verifier/*.jsonl
rm -f /tmp/synced_records.jsonl /tmp/selftest_synced.jsonl

# Phase 1: Run regression selftest against isolated mock instance
SELFTEST_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')
MOCK_LOG_FILE=/logs/verifier/regression_api.jsonl \
  python3 /tests/mock_server.py --port "$SELFTEST_PORT" &
SELFTEST_MOCK_PID=$!
sleep 1

API_BASE="http://127.0.0.1:${SELFTEST_PORT}" \
  timeout 30 python3 /app/sync.py --selftest || true

kill "$SELFTEST_MOCK_PID" 2>/dev/null || true
wait "$SELFTEST_MOCK_PID" 2>/dev/null || true

# Phase 2: Start main mock server for full task execution
MAIN_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')
MOCK_LOG_FILE=/logs/verifier/api_requests.jsonl \
  python3 /tests/mock_server.py --port "$MAIN_PORT" &
MAIN_MOCK_PID=$!
sleep 1

API_BASE="http://127.0.0.1:${MAIN_PORT}" \
  timeout 15 python3 /app/sync.py || true

kill "$MAIN_MOCK_PID" 2>/dev/null || true
wait "$MAIN_MOCK_PID" 2>/dev/null || true

# Phase 3: Evaluate results
python3 /tests/grader.py
