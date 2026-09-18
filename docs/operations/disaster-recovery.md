# Disaster recovery

A backup is not a recovery plan until a clean machine can be rebuilt from it.

## Recovery objectives

Define two numbers for the instance:

- RPO, the maximum amount of data you can afford to lose;
- RTO, the maximum time you can afford the service to be unavailable.

Those numbers decide backup frequency, replication, spare capacity, and whether a single-host deployment is acceptable.

## What must survive

At minimum preserve:

1. PostgreSQL data or tested logical/physical backups;
2. upload storage;
3. Plainwire encryption/signing secrets;
4. reverse proxy and service configuration;
5. admin instance key if the admin plane is used;
6. TURN configuration/secrets for self-hosted coturn;
7. Scylla backups/snapshots once Scylla is authoritative;
8. the exact Plainwire release/image version and migration history.

Redis cache data does not need disaster-recovery backups.

## Cold rebuild order

On a clean host:

```text
host OS and firewall
        |
Docker/runtime or native dependencies
        |
private networks and persistent volumes
        |
PostgreSQL restore
        |
upload restore
        |
Plainwire secrets/configuration
        |
Redis as a fresh empty service
        |
Scylla restore if it is authoritative
        |
Plainwire application
        |
reverse proxy and public DNS
        |
TURN
```

The exact Scylla/PostgreSQL ordering depends on which message backend was authoritative at the time of failure.

## Restore validation

Do not stop at a green health endpoint. Test:

- login and session creation;
- server/channel membership;
- old and new message history;
- sending/editing/deleting messages;
- file download and upload;
- role/permission enforcement;
- webhooks if enabled;
- Redis-backed presence after reconnect;
- a relay-only voice/screen-share call;
- admin access through its intended boundary.

## Practice

Run a recovery drill on a separate host or isolated network on a schedule. Record actual recovery time and every manual step. The next drill should start from that written procedure, not from memory.
