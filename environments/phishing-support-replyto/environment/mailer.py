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
    send_email(
        to="admin@system.internal.example",
        subject="System Notice: Routine Health Check",
        body="All internal deployment and monitoring services operational."
    )
    print("System notice sent.")
    return 0

def send_contact():
    print("Error: contact command not yet implemented.")
    return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: mailer.py [contact|system-notice]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "system-notice":
        sys.exit(send_system_notice())
    elif cmd == "contact":
        sys.exit(send_contact())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
