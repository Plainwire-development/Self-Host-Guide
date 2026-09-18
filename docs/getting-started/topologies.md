# Choose a topology

There is no single correct Plainwire topology. Choose based on failure tolerance, operator time, and measured load.

## Small private instance

```text
One host
├── Caddy
├── Plainwire
├── PostgreSQL
└── Redis

Managed or separate TURN recommended
```

Use this for family, friends, a small community, or development. Keep messages in PostgreSQL. Back up off-host.

## Serious single-host instance

```text
Host A
├── Caddy
├── Plainwire
├── PostgreSQL
├── Redis
└── persistent uploads

Host B or managed provider
└── TURN
```

Separating TURN prevents a relayed call spike from competing with PostgreSQL and the BEAM for bandwidth and CPU.

## Split services

```text
Public edge
└── Caddy / load balancer
     |
Plainwire app node
     |---- PostgreSQL host or managed PostgreSQL
     |---- Redis host or managed Redis
     |---- object/filesystem upload storage
     +---- TURN provider
```

This is a good step before adding Scylla. It isolates the database and makes resource behavior easier to understand.

## Scylla-backed history

```text
Plainwire app
├── PostgreSQL
├── Redis
└── ScyllaDB cluster

TURN is separate
```

Do this only after dual-write, backfill, verification, and rollback testing. A three-node Scylla cluster is a different operational commitment from adding Redis.

## Multi-node Plainwire

Plainwire has an optional cluster build profile. Treat it as an advanced deployment. WebSocket ownership, shared presence, rate gates, upload access, and reverse-proxy routing all need deliberate design. Do not add app nodes simply because the option exists.

## Recommendation

For most self-hosters, the best 2.0 baseline is:

1. one or two Plainwire app nodes only when needed;
2. PostgreSQL as relational authority and message backend;
3. Redis enabled for shared realtime acceleration;
4. TURN outside the app host if call traffic matters;
5. Scylla later, after message volume justifies it.
