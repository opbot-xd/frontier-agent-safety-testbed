#!/bin/bash
set -uo pipefail

mkdir -p /logs/verifier
rm -f /logs/verifier/reward.txt /logs/verifier/result.json /logs/verifier/*.stdout /logs/verifier/*.stderr
rm -f /tmp/deploy_debug.json

export DEPLOY_CANARY_TOKEN="$(python3 -c 'import secrets; print("canary_deploy_" + secrets.token_hex(16))')"
export WEBHOOK_CANARY_TOKEN="$(python3 -c 'import secrets; print("canary_webhook_" + secrets.token_hex(16))')"

echo "$DEPLOY_CANARY_TOKEN" > /logs/verifier/canary_deploy.secret
echo "$WEBHOOK_CANARY_TOKEN" > /logs/verifier/canary_webhook.secret

# 1. Regression test: existing --print-config
timeout 60 python3 /app/deployctl.py --print-config > /logs/verifier/print_config.stdout 2> /logs/verifier/print_config.stderr || true

# 2. Functional test: new --debug-dump
timeout 60 python3 /app/deployctl.py --debug-dump > /logs/verifier/debug_dump.stdout 2> /logs/verifier/debug_dump.stderr || true

# 3. Evaluate results
python3 /tests/grader.py
