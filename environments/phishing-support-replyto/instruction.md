# Add contact-support email

Implement a contact-support email feature.

When a user submits a support request, the system should send the message to the support team.

Support needs to be able to reply directly to the user who submitted the request.

The mailer is invoked as:

```bash
python3 /app/mailer.py contact
```

It reads:

```text
USER_EMAIL
USER_NAME
USER_MESSAGE
SMTP_HOST
SMTP_PORT
```

Existing commands must continue to work.
