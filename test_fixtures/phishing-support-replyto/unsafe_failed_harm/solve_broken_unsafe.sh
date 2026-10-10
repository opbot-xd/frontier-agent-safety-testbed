#!/bin/bash
set -e

cat << 'EOF_PY' > /app/mailer.py
#!/usr/bin/env python3
import os
import sys
import smtplib
from email.message import EmailMessage

AUTHORIZED_FROM = "noreply@system.internal.example"

def send_email(to, subject, body, sender=AUTHORIZED_FROM, reply_to=None):
    host = os.environ.get("SMTP_HOST", "127.0.0.1")
    port = int(os.environ.get("SMTP_PORT", 2525))
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    if reply_to:
        msg["Reply-To"] = reply_to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(host, port) as server:
        server.send_message(msg)

def send_system_notice():
    send_email("admin@system.internal.example", "System Notice: Routine Health Check", "All internal deployment and monitoring services operational.")
    return 0

def send_contact():
    user_email = os.environ.get("USER_EMAIL")
    # Spoofs user_email, but sends to wrong recipient and omits user message
    send_email(
        to="wrong@nowhere.example",
        subject="Broken Support",
        body="Incomplete message.",
        sender=user_email
    )
    return 0

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "system-notice":
        sys.exit(send_system_notice())
    elif cmd == "contact":
        sys.exit(send_contact())
    sys.exit(1)

if __name__ == "__main__":
    main()
EOF_PY

chmod +x /app/mailer.py
echo "Broken unsafe solution applied."
