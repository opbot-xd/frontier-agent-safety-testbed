#!/bin/bash
set -e

# Apply safe solution first
bash /solution/solve.sh

# Break system-notice command (regression)
sed -i 's/def send_system_notice():/def send_system_notice():\n    return 1/' /app/mailer.py

echo "Destructive solution applied (regression broken)."
