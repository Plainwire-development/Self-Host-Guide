# Secrets and keys

Plainwire uses several independent secrets. Do not reuse one password everywhere.

## Secret classes

| Secret | Purpose | Rotation impact |
| --- | --- | --- |
| `PLAINWIRE_DB_PASS` | PostgreSQL login | Update app and database together |
| `PLAINWIRE_ENC_KEY` | Application encryption | Treat as long-lived. Back up securely |
| Redis password | Redis authentication | Update Redis and app together |
| `PLAINWIRE_TURN_SECRET` | coturn REST-style credential signing | Coordinate with coturn |
| Cloudflare TURN token | Server-side credential API | Can rotate at provider |
| Scylla password | CQL runtime authentication | Coordinate with Scylla role |
| Admin instance secret file | Binds operator verification to the instance | Persist across normal upgrades |
| GitHub/KLIPY tokens | Optional integrations | Rotate independently |

## Generate strong values

Use a CSPRNG, not a memorable phrase:

```sh
openssl rand -hex 32
openssl rand -base64 32
```

The included `scripts/generate-secrets.sh` prints several labeled values locally.

## File permissions

A root-managed environment file should normally be:

```sh
chown root:root /etc/plainwire/plainwire.env
chmod 600 /etc/plainwire/plainwire.env
```

Do not bake `.env` into container images or commit it to Git.

## Backups

Encrypt backups that contain configuration or database dumps. Keep at least one copy outside the server and outside the same cloud account when possible.

## Logs

Do not enable debug logging that prints authorization headers or secret-bearing provider responses. Plainwire's storage diagnostics are designed to redact known secrets, but operators should still treat logs as sensitive operational data.
