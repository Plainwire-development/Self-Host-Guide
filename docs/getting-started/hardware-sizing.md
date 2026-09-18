# Hardware and capacity planning

Capacity depends on active users, message rate, upload rate, database layout, and especially how much call traffic is relayed through TURN. Treat these numbers as starting points, then load test.

## Plainwire without Scylla

| Class | CPU | RAM | Disk | Typical use |
| --- | ---: | ---: | ---: | --- |
| Lab | 2 vCPU | 2 to 4 GB | 20 GB SSD | Development, a few accounts |
| Small | 2 to 4 vCPU | 4 to 8 GB | 40 to 100 GB SSD | Small private or community instance |
| Comfortable | 4 to 8 vCPU | 8 to 16 GB | 100 GB+ SSD | Public instance with room for builds and bursts |
| Split services | 4+ vCPU app host | 8+ GB app host | separate DB/upload capacity | Growing deployment |

PostgreSQL and Redis are usually easier to scale vertically before adding application complexity.

## Scylla sizing

ScyllaDB can technically run in small test environments, but production sizing is different. Current Scylla documentation lists 4 GB as a production floor and recommends 16 GB or 2 GB per logical core, whichever is higher. For a Plainwire deployment that is serious enough to need Scylla, plan separate nodes and substantially more headroom than the absolute minimum.

A sensible operator starting point for a real Scylla node is 8 vCPU and 16 GB RAM with fast SSD storage, then size from measured data. Larger workloads should follow Scylla's sizing guidance rather than this handbook.

## TURN sizing

TURN carries media bytes when direct WebRTC connectivity fails. That can dwarf application traffic.

Rough relay bandwidth for a two-party call is approximately the sum of media flowing through the relay in both directions. Group mesh calls multiply traffic because each participant sends to multiple peers.

Example:

```text
4 participants
1.5 Mb/s outgoing media per participant
all paths relayed

rough relay ingress  = 6 Mb/s
rough relay egress   = 18 Mb/s in a full mesh fanout pattern
```

Real behavior depends on codec, browser adaptation, screen share, audio, and how many peer paths actually use TURN. Use provider analytics or host network metrics.

## Disk sizing

Plan separately for:

- PostgreSQL data and WAL;
- upload files;
- backups and temporary restore space;
- container images/build artifacts;
- Scylla data if enabled.

Do not let uploads fill the filesystem that PostgreSQL needs to stay healthy.

## When to scale

Scale because a metric is approaching a limit:

- sustained CPU saturation;
- memory pressure or OOM kills;
- PostgreSQL latency and lock pressure;
- DB pool queue growth;
- Redis timeouts;
- Scylla queue depth or p95 latency;
- WebSocket queue shedding;
- upload I/O saturation;
- TURN network saturation.

More services without measurements can make reliability worse.
