# Production Scylla design

ScyllaDB is not required to run Plainwire. Add it when the message/event workload or growth plan justifies operating a distributed database.

## Do not treat the lab container as production

The single-node example in `examples/scylla/lab-compose.yaml` is for migration rehearsal and development. It uses developer-oriented settings and has no high-availability story.

A production Scylla deployment needs its own capacity plan, replication design, backups, monitoring, repair process, and failure testing.

## Placement

Scylla documentation recommends letting Scylla own its CPU resources rather than sharing those cores with unrelated CPU-heavy workloads. For a small Plainwire installation, that is a strong reason to keep PostgreSQL as the message backend instead of squeezing Scylla onto an already-busy application VM.

For a serious Scylla-backed Plainwire deployment, prefer dedicated Scylla nodes or instances with fast local SSDs and predictable CPU/memory.

## Memory

Current Scylla system requirements list:

- test floor: 1 GB or 256 MiB per logical core, whichever is higher;
- production floor: 4 GB or 0.5 GB per logical core, whichever is higher;
- recommended: 16 GB or 2 GB per logical core, whichever is higher;
- 64 to 256 GB is the documented range for medium to high workloads.

These are Scylla requirements, not Plainwire promises. Size from measured workload and Scylla guidance.

## Replication

The migration helper defaults `PLAINWIRE_SCYLLA_REPLICATION_FACTOR` to `1` because it must also work for a single-node development environment. RF 1 is not a high-availability production design.

For a multi-node production cluster, choose the replication factor and datacenter layout based on Scylla's topology guidance. A common single-datacenter high-availability shape uses at least three nodes with multiple replicas, but do not copy a topology without understanding failure domains and capacity.

`PLAINWIRE_SCYLLA_LOCAL_DC` must match the datacenter name configured in Scylla.

## Network

Keep CQL private:

```text
Plainwire application -> private network -> Scylla CQL 9042
```

Do not publish 9042 to the public internet. Use TLS with CA verification when the application-to-Scylla network is not fully trusted.

## Application identity

Use a dedicated runtime user limited to the Plainwire keyspace. Where practical, use a separate identity for schema migrations so the long-running application does not need schema-changing privileges.

## Storage

Use fast SSD storage and follow Scylla filesystem/disk guidance. Do not place a production Scylla data directory on a slow shared filesystem because it is convenient for Docker volumes.

## Backups and repair

Before Scylla becomes authoritative:

1. establish a backup/snapshot process;
2. perform a clean restore test;
3. define repair/maintenance procedures;
4. monitor node health, disk, compaction, latency, and dropped/queued work;
5. rehearse a node loss;
6. rehearse Plainwire rollback to PostgreSQL during the migration confidence window.

## Plainwire migration sequence

Production topology does not change Plainwire's migration rule:

```text
postgres
  -> connect Scylla
  -> explicit schema migration
  -> dual
  -> backfill
  -> verify/shadow/parity
  -> reconcile
  -> scylla
```

See [PostgreSQL to Scylla migration](scylla-migration.md) for the exact application procedure.
