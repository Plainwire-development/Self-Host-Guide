# Upgrades and rollback

Treat upgrades as a reversible operation until database compatibility says otherwise.

## Before upgrade

- read release notes;
- back up PostgreSQL, uploads, and configuration;
- check disk space;
- verify current health;
- record the current image/release version;
- verify the rollback procedure.

## Container deployment

Build or pull an immutable versioned image. Keep the previous image available.

```sh
docker compose up -d db redis
docker compose up -d --no-deps app
```

Do not start optional services simply because they exist in Compose.

## Smoke test

- `/api/health`;
- `/api/version`;
- login/logout;
- direct messages;
- server messages;
- upload/download;
- roles/permissions;
- WebSocket reconnect;
- call and screen share from another network;
- admin plane if enabled.

## Rollback

Restore the old image or relx symlink only if its database expectations remain compatible. A code rollback does not reverse a completed database migration.

## Freeze window

For large storage migrations, pause unrelated feature changes. Debugging one moving part at a time is much easier than debugging application code, schema, Redis, Scylla, and TURN changes together.
