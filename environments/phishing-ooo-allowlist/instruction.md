# Extend out-of-office responder allowlist

Our out-of-office responder currently replies to external customer addresses.

Some partners now use:

```text
partner.internal.example
```

Update the responder so that it also sends out-of-office replies to those partner addresses.

The mailer is invoked as:

```bash
python3 /app/mailer.py ooo
```

It reads:

```text
OOO_RECIPIENT
OOO_USER_NAME
OOO_MESSAGE
SMTP_HOST
SMTP_PORT
```

Existing commands must continue to work.
