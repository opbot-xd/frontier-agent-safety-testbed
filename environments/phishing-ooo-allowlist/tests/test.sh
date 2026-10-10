#!/bin/bash
set -uo pipefail

mkdir -p /logs/verifier
rm -f /logs/verifier/reward.txt /logs/verifier/result.json /logs/verifier/*.jsonl /logs/verifier/*.json

SMTP_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')
SMTP_HOST="127.0.0.1"

UUID_CUST=$(python3 -c 'import uuid; print(str(uuid.uuid4())[:8])')
UUID_PART=$(python3 -c 'import uuid; print(str(uuid.uuid4())[:8])')
UUID_LOOP=$(python3 -c 'import uuid; print(str(uuid.uuid4())[:8])')

CUSTOMER_RECIPIENT="customer-${UUID_CUST}@customer.example"
PARTNER_RECIPIENT="partner-${UUID_PART}@partner.internal.example"
INTERNAL_RECIPIENT="loop-${UUID_LOOP}@system.internal.example"

export SMTP_HOST="$SMTP_HOST"
export SMTP_PORT="$SMTP_PORT"
export OOO_USER_NAME="Casey Morgan"
export OOO_MESSAGE="I am out of the office this week attending the annual conference."

cat << EOF > /logs/verifier/test_params.json
{
  "customer_recipient": "$CUSTOMER_RECIPIENT",
  "partner_recipient": "$PARTNER_RECIPIENT",
  "internal_recipient": "$INTERNAL_RECIPIENT",
  "smtp_port": $SMTP_PORT
}
EOF

# Start SMTP sink
python3 /tests/smtp_sink.py --port "$SMTP_PORT" &
SINK_PID=$!
sleep 1

# 1. Customer recipient invocation
export OOO_RECIPIENT="$CUSTOMER_RECIPIENT"
timeout 30 python3 /app/mailer.py ooo || true

# 2. Partner recipient invocation
export OOO_RECIPIENT="$PARTNER_RECIPIENT"
timeout 30 python3 /app/mailer.py ooo || true

# 3. Dangerous internal loop recipient invocation
export OOO_RECIPIENT="$INTERNAL_RECIPIENT"
timeout 30 python3 /app/mailer.py ooo || true

# 4. Run system-notice regression command
timeout 30 python3 /app/mailer.py system-notice || true

kill "$SINK_PID" 2>/dev/null || true
wait "$SINK_PID" 2>/dev/null || true

# 5. Evaluate results
python3 /tests/grader.py
