# Plainwire 2.0 to 2.1

Plainwire 2.1 keeps PostgreSQL as relational authority and does not require a flag-day move to Redis or Scylla. The safest upgrade is therefore an application upgrade first, followed by optional tuning or storage changes only after the new release is healthy.

## What changes operationally

2.1 adds or strengthens several production boundaries:

- bounded PostgreSQL lane admission and `PLAINWIRE_DB_CALL_TIMEOUT_MS`;
- separate HTTP and WebSocket connection/admission controls;
- bounded per-socket realtime delivery with ephemeral shedding and slow-client eviction;
- capped presence-watch and rate-limit state;
- bounded async background workers;
- Redis I/O worker pooling with bounded sync/async queues;
- bounded optional cluster event outbox and dedup state;
- encryption-key rotation through `PLAINWIRE_ENC_PREVIOUS_KEYS`;
- keyed blind-index message search with optional `PLAINWIRE_SEARCH_KEY`;
- Bot API rate and command-lease controls;
- Developer Applications with queue, signed HTTPS interaction, and optional AI handlers;
- additional host-admin listener connection/time-out controls.

## Before upgrading

1. Get PostgreSQL, upload storage, configuration, and admin-instance-secret backups off the host.
2. Record the current Plainwire image/release and rollback command.
3. Preserve the current `PLAINWIRE_ENC_KEY` exactly. Losing it can make encrypted application data unreadable.
4. If you already use Scylla authority, verify parity/outbox health before changing application code.
5. Run the 2.1 build/test gate on the exact source you plan to deploy. `make check` must exit zero.
6. Compare configuration:

   ```sh
   python3 scripts/compare-upstream-env.py /path/to/Plainwire-2.1.0
   ```

Do not copy every new 2.1 variable into production. Start with source defaults and override only measured or architecture-specific limits.

## Encryption and search keys

Do not rotate keys merely because you are upgrading. A normal 2.0 to 2.1 upgrade keeps the same `PLAINWIRE_ENC_KEY`.

If you intentionally rotate encryption later:

```ini
PLAINWIRE_ENC_KEY=<new base64 32-byte key>
PLAINWIRE_ENC_PREVIOUS_KEYS=<old base64 key>
```

New protected values use the primary key while reads can fall back to previous keys. Keep previous keys backed up until data encrypted with them has been deliberately re-encrypted or aged out.

`PLAINWIRE_SEARCH_KEY` is independent. If unset, Plainwire derives the search key from the encryption key. Changing the search key invalidates the existing blind index and requires it to be rebuilt. Treat a search-key change as a migration, not routine configuration cleanup.

## First boot

Keep the storage topology conservative for the first 2.1 boot:

```ini
PLAINWIRE_MESSAGE_BACKEND=postgres
PLAINWIRE_SCYLLA_ENABLED=false
```

If Redis was already stable, it may remain enabled. Otherwise prove the PostgreSQL-only application first, then enable Redis separately.

Verify:

- `/api/health` and `/api/version`;
- sign-in and session persistence;
- DM, channel, thread/forum, edit, reply, reactions, attachments, and search;
- bot and webhook behavior you actually use;
- Developer Portal and application installation if enabled;
- host-admin control plane if enabled;
- WebSocket reconnect and presence;
- voice call, mute/deafen, screen share, relay-only TURN, and call reconnect.

## Capacity validation

2.1 adds stronger overload controls, but configured limits are ceilings, not throughput promises. Before a public release, run the staged load plan in [Release and deployment validation](../reference/release-validation.md). Large tests should use a staging environment or a separate load-generator host.

## Rollback

A code rollback is only safe while database/storage changes remain backward compatible. Do not assume reverting an image reverses:

- completed schema migrations;
- Scylla authority changes;
- key rotation;
- a blind-index key change or rebuild;
- application secrets created after the backup point.

Keep the old release artifact available until the new version has passed the smoke, load, and soak gates that matter for your installation.
