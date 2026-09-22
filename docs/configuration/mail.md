# Mail

Password reset and email verification stay off on a self-hosted Plainwire instance until you turn them on. The official `plainwi.re` host is the exception: if `PLAINWIRE_MAIL_ENABLED` is unset and SMTP is configured, mail turns on there by itself.

## Enable mail

All of the following have to be true:

- `PLAINWIRE_MAIL_ENABLED=true`;
- `PLAINWIRE_SMTP_HOST`, `PLAINWIRE_SMTP_USER`, and `PLAINWIRE_SMTP_PASS` are set;
- `PLAINWIRE_PUBLIC_URL` is set, because links in the message use it.

```ini
PLAINWIRE_MAIL_ENABLED=true
PLAINWIRE_PUBLIC_URL=https://chat.example.com
PLAINWIRE_SMTP_HOST=smtp.example.com
PLAINWIRE_SMTP_PORT=587
PLAINWIRE_SMTP_USER=mailer@example.com
PLAINWIRE_SMTP_PASS=CHANGE_ME
PLAINWIRE_SMTP_FROM=mailer@example.com
PLAINWIRE_SMTP_TLS=true
```

`PLAINWIRE_SMTP_PORT` defaults to 587. `PLAINWIRE_SMTP_TLS` defaults to true. If `PLAINWIRE_SMTP_FROM` is empty, Plainwire uses `PLAINWIRE_SMTP_USER`.

Set `PLAINWIRE_MAIL_ENABLED` to `false`, `0`, `no`, or `off` to keep mail off, including on a host whose public URL is `plainwi.re`.

Put the SMTP password in the private environment file. The upstream example uses `smtp.protonmail.ch` as a sample host. Proton needs an SMTP token from Proton settings, not the mailbox password. Use the host, port, and credentials your provider documents.

## What a message can do

A reset link is sent only to a verified address. An account with no email cannot reset its password. Verification links are valid for 24 hours. Reset links are valid for 1 hour.

Outgoing headers have CR and LF removed. Body lines are dot-stuffed so a lone `.` is not treated as the end of the SMTP message.

## Operator resend

The host control plane can queue another verification message with `POST /api/users/:id/moderation` and action `resend_verification`. That action runs only when mail is enabled on this host. It is limited to 4 attempts per account per 10 minutes. The one-time token is not returned to the browser, and the panel does not show the address.

See [Host admin control plane](admin-control-plane.md).
