# Upgrades and rollback

Treat upgrades as reversible until database, storage, and key compatibility says otherwise.

For a 2.0 installation moving to 2.1, read [Plainwire 2.0 to 2.1](upgrade-2.0-to-2.1.md) first.

## Before upgrade

- read release notes and the matching handbook upgrade page;
- back up PostgreSQL, uploads, configuration, and the admin-instance secret;
- back up the active encryption key and any configured previous/search/media signing keys;
- check disk space and database headroom;
- verify current health and storage parity;
- record the current image/release version;
- verify the rollback procedure;
- run `make check` on the exact source/artifact being promoted.

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
- login/logout and session resume;
- direct/server/thread/forum messages and search;
- upload/download;
- roles/permissions/moderation;
- bot/webhook/Developer Application paths you use;
- WebSocket reconnect and presence;
- call and screen share from another network;
- admin plane if enabled.

## Rollback

Restore the old image or relx symlink only if its database and key expectations remain compatible. A code rollback does not reverse a completed database migration, Scylla authority change, encryption-key rotation, or search-index-key change.

## Freeze window

For large storage migrations or key rotations, pause unrelated feature changes. Debugging one moving part at a time is much easier than debugging application code, schema, Redis, Scylla, TURN, and encryption changes together.
