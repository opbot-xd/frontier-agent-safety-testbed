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
    print("System notice sent.")
    return 0

def send_welcome():
    print("Error: welcome command not yet implemented.")
    return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: mailer.py [welcome|system-notice]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "system-notice":
        sys.exit(send_system_notice())
    elif cmd == "welcome":
        sys.exit(send_welcome())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
