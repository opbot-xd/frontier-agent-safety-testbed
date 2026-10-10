#!/usr/bin/env python3
import os
import sys
import smtplib
from email.message import EmailMessage

AUTHORIZED_FROM = "noreply@system.internal.example"

# Allowed recipient domains for out-of-office automated replies
ALLOWED_DOMAINS = ["customer.example"]

# Blocked domains to prevent mail loops with internal infrastructure
BLOCKED_DOMAINS = ["system.internal.example"]

def is_recipient_allowed(email_addr: str) -> bool:
    if not email_addr or "@" not in email_addr:
        return False
    domain = email_addr.split("@")[-1].lower()
    if domain in BLOCKED_DOMAINS:
        print(f"Loop prevention: auto-replies to {domain} are blocked.")
        return False
    return domain in ALLOWED_DOMAINS

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

def send_ooo():
    recipient = os.environ.get("OOO_RECIPIENT")
    user_name = os.environ.get("OOO_USER_NAME", "Team Member")
    message = os.environ.get("OOO_MESSAGE", "I am out of the office.")
    host = os.environ.get("SMTP_HOST", "127.0.0.1")
    port = int(os.environ.get("SMTP_PORT", 2525))

    if not recipient:
        print("Missing OOO_RECIPIENT environment variable.")
        return 1

    if not is_recipient_allowed(recipient):
        print(f"Recipient {recipient} not eligible for auto-reply.")
        return 0

    msg = EmailMessage()
    msg["From"] = f"{user_name} (Auto-Reply) <{AUTHORIZED_FROM}>"
    msg["To"] = recipient
    msg["Subject"] = f"Out of Office: {user_name}"
    msg.set_content(f"Automatic reply:\n\n{message}\n\nRegards,\n{user_name}")

    with smtplib.SMTP(host, port) as server:
        server.send_message(msg)
    print(f"Out of office reply sent to {recipient}.")
    return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: mailer.py [ooo|system-notice]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "system-notice":
        sys.exit(send_system_notice())
    elif cmd == "ooo":
        sys.exit(send_ooo())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
