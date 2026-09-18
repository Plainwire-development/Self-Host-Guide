# PostgreSQL to Scylla migration

Do not switch an existing instance directly from PostgreSQL to Scylla.

## Phase 0: healthy PostgreSQL

```ini
PLAINWIRE_MESSAGE_BACKEND=postgres
PLAINWIRE_SCYLLA_ENABLED=false
```

Take backups and verify messages, uploads, and account operations.

## Phase 1: create schema

Configure Scylla connectivity, then run:

```sh
PLAINWIRE_SCYLLA_LOCAL_DC=datacenter1 \
PLAINWIRE_SCYLLA_REPLICATION_FACTOR=3 \
./scripts/scylla-migrate
```

Use replication factor 1 only for a single-node test system. A three-node single-DC cluster normally uses RF 3.

Enable connectivity while messages remain PostgreSQL-backed:

```ini
PLAINWIRE_SCYLLA_ENABLED=true
PLAINWIRE_MESSAGE_BACKEND=postgres
```

Check storage health.

## Phase 2: dual write

```ini
PLAINWIRE_MESSAGE_BACKEND=dual
```

New message work commits to PostgreSQL first and is mirrored to Scylla through the durable outbox.

## Phase 3: backfill

```sh
./scripts/storage-migrate status
./scripts/storage-migrate backfill 50000
```

Backfill progress is checkpointed. Reruns resume.

## Phase 4: verify

```sh
./scripts/storage-migrate verify 0 1000
./scripts/storage-migrate shadow 500
./scripts/storage-migrate parity 500
./scripts/storage-migrate flush-outbox
```

A successful process exit is not enough. Review mismatch counts, backlog, latency, and health.

If needed:

```sh
./scripts/storage-migrate reconcile-intents 500
./scripts/storage-migrate reconcile 500
```

## Phase 5: make Scylla authoritative

Only after backfill is complete, outbox is caught up, repeated verification is clean, and operational metrics are acceptable:

```ini
PLAINWIRE_MESSAGE_BACKEND=scylla
```

Keep PostgreSQL message rows through a confidence window.

## Rollback

```ini
PLAINWIRE_MESSAGE_BACKEND=postgres
```

Restart normally. Do not delete the PostgreSQL recovery mirror during initial Scylla adoption.
