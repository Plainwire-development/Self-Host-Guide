# PostgreSQL

PostgreSQL is mandatory in Plainwire 2.5. It remains relational authority even when Scylla stores the canonical high-volume message timeline. Redis and ScyllaDB stay optional. Existing installs apply pending migrations, including migration 53, when the database process starts.

## What PostgreSQL owns

- users and account state;
- servers, channels, memberships;
- roles and permissions;
- bot and webhook configuration;
- sessions and transactional metadata;
- default message storage;
- Scylla migration checkpoints, outbox, and recovery metadata.

## Version policy

Use a currently supported PostgreSQL major release and stay current on its minor releases. The upstream development Compose file uses PostgreSQL 18. Do not infer that every production deployment must upgrade immediately to 18 without testing.

## Dedicated role

Use a dedicated database and runtime role. Do not run Plainwire as the PostgreSQL superuser.

## TLS

For a database over an untrusted or shared network:

```ini
PLAINWIRE_DB_SSL=true
```

Plainwire production configuration intentionally resists insecure remote database setups. `PLAINWIRE_ALLOW_INSECURE_DB` should be reserved for a database isolated on a trusted local/private network when you understand the risk.

## Pool sizing

The upstream example starts around twice CPU count and suggests measuring before tuning:

```ini
PLAINWIRE_DB_POOL_SIZE=20
PLAINWIRE_DB_MAX_QUEUE=250
PLAINWIRE_DB_STATEMENT_TIMEOUT_MS=15000
PLAINWIRE_DB_IDLE_TX_TIMEOUT_MS=15000
PLAINWIRE_DB_LOCK_TIMEOUT_MS=5000
PLAINWIRE_DB_SLOW_MS=250
```

More connections do not automatically mean more throughput. PostgreSQL has its own connection, memory, and I/O limits.

## Backup

Use logical dumps, physical backups, managed snapshots, or a tested combination appropriate to your deployment. A filesystem copy of a live PostgreSQL data directory is not a complete backup strategy by itself.
