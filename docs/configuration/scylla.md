# ScyllaDB

ScyllaDB is optional. Use it when the message and event timeline is large enough to justify a separate distributed database.

## Storage split

```text
PostgreSQL   relational authority
Redis        ephemeral realtime acceleration
ScyllaDB     ordered high-volume history
```

PostgreSQL remains mandatory after Scylla is enabled.

## Runtime modes

```ini
PLAINWIRE_MESSAGE_BACKEND=postgres
```

PostgreSQL owns message reads and writes. This is the default and rollback mode.

```ini
PLAINWIRE_MESSAGE_BACKEND=dual
```

PostgreSQL stays read authority. New durable work is mirrored through a PostgreSQL outbox to Scylla. Use this for migration, not steady state.

```ini
PLAINWIRE_MESSAGE_BACKEND=scylla
```

Scylla becomes canonical message timeline read authority. PostgreSQL remains relational authority and recovery mirror during the confidence window.

## Core settings

```ini
PLAINWIRE_SCYLLA_ENABLED=true
PLAINWIRE_SCYLLA_CONTACT_POINTS=scylla-1.internal,scylla-2.internal,scylla-3.internal
PLAINWIRE_SCYLLA_PORT=9042
PLAINWIRE_SCYLLA_KEYSPACE=plainwire
PLAINWIRE_SCYLLA_LOCAL_DC=datacenter1
PLAINWIRE_SCYLLA_CONSISTENCY=local_quorum
```

Use TLS with CA verification across untrusted networks. Do not expose CQL port 9042 publicly.

## Production shape

The upstream Compose Scylla service is explicitly for development. A production Scylla cluster needs appropriate CPU isolation, memory, fast SSD storage, filesystem setup, replication, monitoring, backups, repair policy, and tested failure behavior.

Current Scylla guidance recommends at least 16 GB or 2 GB per logical core for a well-sized node, with a much lower absolute production floor. If you are operating Scylla because Plainwire has become large, size for the workload rather than the floor.

## Backpressure

Plainwire puts bounded queues and per-partition limits in front of Scylla. Keep the defaults until metrics prove they need tuning. Raising queue limits can convert a short overload into a long memory problem.

## Schema

Application startup does not create or alter Scylla schema. Run the migration tool explicitly.

Continue with [PostgreSQL to Scylla migration](scylla-migration.md).
