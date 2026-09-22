# Performance tuning

Tune from evidence. Plainwire 2.5 bounds the main queues/admission paths so overload can fail predictably instead of filling memory forever. Raising every ceiling is not a scaling strategy.

## Erlang runtime

The upstream production example uses:

```ini
ERL_FLAGS=+S auto +A 64 +P 2000000 +sbwt very_short +sbwtdcpu very_short +sbwtdio short
```

Do not cargo-cult VM flags onto tiny hosts. Measure scheduler utilization, run queue, memory, process count, and latency.

## HTTP listener

```ini
PLAINWIRE_HTTP_ACCEPTORS=100
PLAINWIRE_HTTP_CONNECTION_SUPERVISORS=8
PLAINWIRE_HTTP_MAX_CONNECTIONS=100000
PLAINWIRE_HTTP_HANDSHAKE_TIMEOUT_MS=5000
PLAINWIRE_HTTP_SEND_TIMEOUT_MS=15000
PLAINWIRE_HTTP_IDLE_TIMEOUT_MS=60000
PLAINWIRE_HTTP_REQUEST_TIMEOUT_MS=30000
PLAINWIRE_HTTP_MAX_KEEPALIVE=1000
```

Host file-descriptor limits, reverse-proxy limits, Ranch capacity, and the configured connection target must agree.

## WebSocket admission and backpressure

```ini
PLAINWIRE_WS_MAX_CONNECTIONS=100000
PLAINWIRE_WS_UPGRADES_PER_IP_MIN=1200
PLAINWIRE_WS_UPGRADES_GLOBAL_MIN=60000
PLAINWIRE_PRESENCE_WATCH_MAX=2000
PLAINWIRE_RATE_MAX_ENTRIES=500000
PLAINWIRE_WS_SOFT_QUEUE=500
PLAINWIRE_WS_HARD_QUEUE=2000
PLAINWIRE_WS_TRACE=false
```

At the soft queue limit, disposable presence/typing/activity traffic may be shed. Persistently slow consumers are evicted at the hard limit. This is intentional overload behavior. Do not interpret a higher hard limit as free throughput.

## Background work

```ini
PLAINWIRE_ASYNC_WORKERS=16
PLAINWIRE_ASYNC_MAX_QUEUE=4096
```

Background presence reads, fanout helpers, missed-call persistence, and similar work should remain bounded. Watch queue saturation before increasing worker count.

## PostgreSQL

Useful controls include:

```ini
PLAINWIRE_DB_POOL_SIZE=20
PLAINWIRE_DB_MAX_QUEUE=250
PLAINWIRE_DB_CALL_TIMEOUT_MS=60000
PLAINWIRE_DB_STATEMENT_TIMEOUT_MS=15000
```

Statement timeout should normally remain below caller timeout. More pool connections can increase contention and consume PostgreSQL connection headroom needed for migrations and maintenance.

## Redis

```ini
PLAINWIRE_REDIS_POOL_SIZE=8
PLAINWIRE_REDIS_SYNC_QUEUE=2048
PLAINWIRE_REDIS_ASYNC_QUEUE=4096
```

Redis is an accelerator, not durable authority. Same-key work is kept ordered through worker affinity, while optional async accelerator work can be shed under overload. A larger queue is not a substitute for fixing a slow Redis path.

## Cluster event transport

If the optional cluster profile is used, watch outbox depth, event age, retries, and duplicate suppression. `PLAINWIRE_CLUSTER_OUTBOX_LIMIT` exists to prevent a transport outage from becoming unbounded BEAM memory growth. See [Optional clustering](clustering.md).

## Scylla

Watch partition hotspots, gate queue depth, operation latency, write-intent/outbox recovery, and dropped/load-shed requests. Do not solve overload by simply raising every queue.

## Voice

Plainwire 2.5 calls are full mesh. Browser CPU, uplink, downlink, and peer count rise rapidly with participants. Keep the default room cap unless real multi-client media testing proves a higher number is acceptable. TURN improves reachability; it does not turn mesh into an SFU.

## Validate changes

After tuning, rerun `make check` and staged load tests. A change that improves peak operations/sec but causes memory not to settle, queue recovery to fail, or p99 latency to explode is not an improvement.
