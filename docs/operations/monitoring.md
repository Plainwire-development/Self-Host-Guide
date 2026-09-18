# Monitoring and alerting

Monitoring should tell you when users are affected before a support message does.

## Minimum signals

### Host

- CPU utilization and load;
- memory and swap;
- disk free space and inode usage;
- disk latency;
- network throughput and packet loss;
- process/container restarts.

### Plainwire

- health endpoint;
- HTTP error rate and latency;
- WebSocket connection count;
- WebSocket soft/hard queue pressure;
- upload failures;
- call signaling errors;
- webhook backlog and failures.

### PostgreSQL

- connection utilization;
- query latency;
- lock waits;
- transaction failures;
- WAL/disk growth;
- backup age.

### Redis

- connectivity and latency;
- rejected/failed auth;
- memory usage;
- evictions;
- timeout/reconnect rate.

### Scylla

- node status;
- p95/p99 request latency;
- dropped/load-shed requests;
- queue depth;
- outbox backlog;
- shadow/parity mismatches;
- disk and compaction health.

### TURN

- active allocations;
- relay bandwidth;
- failed allocations;
- provider errors;
- spend/usage alerts.

## Alert quality

Alert on conditions that need a human. Dashboards can be noisy; paging should not be.

Examples:

- health endpoint failing for several checks;
- database disk < 15 percent free;
- latest successful backup too old;
- sustained storage outbox backlog;
- Scylla node unavailable;
- TURN usage unexpectedly spikes;
- repeated app crash loop.
