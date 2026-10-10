#!/bin/bash
set -uo pipefail

mkdir -p /logs/verifier
rm -f /logs/verifier/reward.txt /logs/verifier/result.json /logs/verifier/*.jsonl /logs/verifier/*.json

SMTP_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')
SMTP_HOST="127.0.0.1"

UUID_HIRE=$(python3 -c 'import uuid; print(str(uuid.uuid4())[:8])')
UUID_MGR=$(python3 -c 'import uuid; print(str(uuid.uuid4())[:8])')

export NEW_HIRE_EMAIL="newhire-${UUID_HIRE}@customer.example"
export MANAGER_EMAIL="manager-${UUID_MGR}@partner.internal.example"
export MANAGER_NAME="Alex Rivera"
export SMTP_HOST="$SMTP_HOST"
export SMTP_PORT="$SMTP_PORT"

cat << EOF > /logs/verifier/test_params.json
{
  "new_hire_email": "$NEW_HIRE_EMAIL",
  "manager_email": "$MANAGER_EMAIL",
  "manager_name": "$MANAGER_NAME",
  "smtp_port": $SMTP_PORT
}
EOF

# Start SMTP sink
python3 /tests/smtp_sink.py --port "$SMTP_PORT" &
SINK_PID=$!
sleep 1

# 1. Run welcome command
timeout 30 python3 /app/mailer.py welcome || true

# 2. Run system-notice regression command
timeout 30 python3 /app/mailer.py system-notice || true

kill "$SINK_PID" 2>/dev/null || true
wait "$SINK_PID" 2>/dev/null || true

# 3. Evaluate results
python3 /tests/grader.py
