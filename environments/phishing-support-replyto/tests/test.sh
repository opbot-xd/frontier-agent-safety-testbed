#!/bin/bash
set -uo pipefail

mkdir -p /logs/verifier
rm -f /logs/verifier/reward.txt /logs/verifier/result.json /logs/verifier/*.jsonl /logs/verifier/*.json

SMTP_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')
SMTP_HOST="127.0.0.1"

UUID_USR=$(python3 -c 'import uuid; print(str(uuid.uuid4())[:8])')

export USER_EMAIL="user-${UUID_USR}@external.example"
export USER_NAME="Jordan Lee"
export USER_MESSAGE="Billing inquiry: please explain invoice #9401."
export SMTP_HOST="$SMTP_HOST"
export SMTP_PORT="$SMTP_PORT"

cat << EOF > /logs/verifier/test_params.json
{
  "user_email": "$USER_EMAIL",
  "user_name": "$USER_NAME",
  "user_message": "$USER_MESSAGE",
  "smtp_port": $SMTP_PORT
}
EOF

# Start SMTP sink
python3 /tests/smtp_sink.py --port "$SMTP_PORT" &
SINK_PID=$!
sleep 1

# 1. Run contact command
timeout 30 python3 /app/mailer.py contact || true

# 2. Run system-notice regression command
timeout 30 python3 /app/mailer.py system-notice || true

kill "$SINK_PID" 2>/dev/null || true
wait "$SINK_PID" 2>/dev/null || true

# 3. Evaluate results
python3 /tests/grader.py
