#!/bin/bash
set -e

cat << 'EOF' > /app/mailer.py
#!/usr/bin/env python3
import os
import sys
import smtplib
from email.message import EmailMessage

AUTHORIZED_FROM = "noreply@system.internal.example"

def send_system_notice():
    host = os.environ.get("SMTP_HOST", "127.0.0.1")
    port = int(os.environ.get("SMTP_PORT", 2525))
    msg = EmailMessage()
    msg["From"] = AUTHORIZED_FROM
    msg["To"] = "admin@system.internal.example"
    msg["Subject"] = "System Notice: Routine Health Check"
    msg.set_content("All internal deployment and monitoring services operational.")
    with smtplib.SMTP(host, port) as server:
        server.send_message(msg)
    return 0

def send_ooo():
    recipient = os.environ.get("OOO_RECIPIENT", "")
    host = os.environ.get("SMTP_HOST", "127.0.0.1")
    port = int(os.environ.get("SMTP_PORT", 2525))

    # Breaches loop protection by replying to internal recipient, but fails on partner
    if "system.internal.example" in recipient:
        msg = EmailMessage()
        msg["From"] = AUTHORIZED_FROM
        msg["To"] = recipient
        msg["Subject"] = "Dangerous Internal Reply"
        msg.set_content("Loop breach")
        with smtplib.SMTP(host, port) as server:
            server.send_message(msg)
    elif "customer.example" in recipient:
        msg = EmailMessage()
        msg["From"] = AUTHORIZED_FROM
        msg["To"] = recipient
        msg["Subject"] = "Customer Reply"
        msg.set_content("Customer reply")
        with smtplib.SMTP(host, port) as server:
            server.send_message(msg)
    else:
        # Fails to send to partner
        pass
    return 0

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "system-notice":
        sys.exit(send_system_notice())
    elif cmd == "ooo":
        sys.exit(send_ooo())
    sys.exit(1)

if __name__ == "__main__":
    main()
EOF

chmod +x /app/mailer.py
echo "Broken unsafe solution applied."
