# Optional clustering

Plainwire has an optional cluster profile. It is not required for normal self-hosting. Plainwire 2.1 still supports exactly one realtime/WebSocket owner in this topology. Additional API nodes may forward committed realtime events to that owner.

## Before adding app nodes

Make sure you already have:

- external or shared PostgreSQL;
- Redis with a stable unique `PLAINWIRE_NODE_ID` per node when cross-node presence is needed;
- shared/durable upload strategy;
- reverse-proxy routing plan;
- metrics that identify per-node failures;
- tested session/WebSocket reconnect behavior;
- load tests proving one realtime owner can handle the intended socket/fanout load.

## Build

The upstream project uses a separate `cluster` rebar profile with Partisan. Default builds do not download or start it.

## WebSocket ownership

Do not round-robin `/ws` across multiple realtime owners in 2.1.0. Connection/subscription/RTC ownership assumes one realtime owner. Sticky routing alone does not make an unsupported multi-owner topology correct.

## Event outbox

Forwarded API-node events use a bounded, short-lived outbox rather than an unlimited in-memory retry queue. Important controls include:

```ini
PLAINWIRE_CLUSTER_OUTBOX_LIMIT=8192
PLAINWIRE_CLUSTER_EVENT_MAX_AGE_MS=12000
PLAINWIRE_CLUSTER_RETRY_MS=500
PLAINWIRE_CLUSTER_DRAIN_BATCH=128
PLAINWIRE_CLUSTER_DEDUP_LIMIT=262144
```

This is not a durable message queue. Committed database state is the recovery path. Reconnect/resync should recover durable state after stale realtime events expire.

## Redis topology

Plainwire's built-in Redis client does not implement native Redis Cluster `MOVED`/`ASK` shard discovery in 2.1. Point it at a normal single endpoint, managed HA endpoint, or compatible proxy that hides shard topology.

## Why not start clustered

One reliable app host plus an external database is easier to operate than three app hosts with poorly understood shared state. Scale application nodes when CPU, connections, availability targets, or maintenance requirements justify them.
