# Performance tuning

Tune from evidence. Plainwire already bounds many queues so overload fails predictably instead of filling memory forever.

## Erlang runtime

The upstream production example uses:

```ini
ERL_FLAGS=+S auto +A 64 +P 2000000 +sbwt very_short +sbwtdcpu very_short +sbwtdio short
```

Do not cargo-cult VM flags onto tiny hosts. Measure scheduler utilization, memory, and latency.

## HTTP

```ini
PLAINWIRE_HTTP_ACCEPTORS=100
PLAINWIRE_HTTP_MAX_CONNECTIONS=100000
PLAINWIRE_HTTP_IDLE_TIMEOUT_MS=60000
PLAINWIRE_HTTP_REQUEST_TIMEOUT_MS=30000
PLAINWIRE_HTTP_MAX_KEEPALIVE=1000
```

Host file-descriptor limits and reverse-proxy limits must agree.

## WebSocket backpressure

```ini
PLAINWIRE_WS_SOFT_QUEUE=500
PLAINWIRE_WS_HARD_QUEUE=2000
```

A slow client should not be allowed to fill a BEAM mailbox forever.

## PostgreSQL

Tune pool size and slow-query thresholds from observed query latency. More pool connections can increase contention.

## Redis

Keep timeouts short. Redis is an accelerator, so the application should not wait seconds for a cache path.

## Scylla

Watch partition hotspots, gate queue depth, operation latency, and dropped/load-shed requests. Do not solve overload by simply raising every queue.

## Voice

Plainwire calls are mesh. Browser and network load rises rapidly with participants. Keep the default room cap unless testing proves a higher number is acceptable.
