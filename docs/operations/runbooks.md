# Failure runbooks

Runbooks turn outages into a sequence of known actions. Adapt these to your monitoring and deployment tooling before launch.

## PostgreSQL unavailable

Impact: authentication, relational state, message storage in the default backend, and most writes are unavailable.

1. Stop repeated destructive restart loops.
2. Check PostgreSQL process/container health and disk space.
3. Check connection count, locks, WAL/disk pressure, and recent config changes.
4. Confirm Plainwire is using the expected host, database, TLS mode, and credentials.
5. Restore database service before trying application-level repairs.
6. If corruption or data loss is suspected, preserve the failed volume and follow the restore runbook.
7. After recovery, verify login, server membership, message send/read, uploads, and migrations.

Do not promote Redis or Scylla into a replacement relational database during an incident.

## Redis unavailable

Impact: distributed realtime acceleration degrades. Plainwire is designed to fall back to local behavior for supported Redis paths.

1. Confirm the Plainwire application remains healthy.
2. Check Redis network reachability and authentication.
3. Check memory pressure, maxmemory behavior, and restart history.
4. Restore Redis.
5. Watch for reconnect success and presence/cache repopulation.

Redis is disposable in the Plainwire design. Do not restore stale cache data merely because a backup exists.

## Scylla unavailable while backend is `postgres`

Impact: usually none to primary message reads/writes. Migration/verification work may fail or queue.

1. Leave `PLAINWIRE_MESSAGE_BACKEND=postgres`.
2. Repair Scylla separately.
3. Check outbox/reconciliation state before resuming migration.

## Scylla unavailable while backend is `dual`

PostgreSQL remains read authority. Preserve the PostgreSQL outbox and do not skip reconciliation to make dashboards green.

1. Repair Scylla.
2. Inspect migration status.
3. Flush/reconcile the outbox.
4. Run parity/verification again before moving forward.

## Scylla unavailable while backend is `scylla`

If the outage is not immediately recoverable and PostgreSQL is still a valid recovery mirror, switch back deliberately:

```ini
PLAINWIRE_MESSAGE_BACKEND=postgres
```

Redeploy, validate message history, then investigate Scylla offline. The exact rollback decision depends on how long Scylla has been authoritative and whether PostgreSQL has remained synchronized.

## Disk nearly full

1. Identify which filesystem is full.
2. Stop uncontrolled growth before deleting data.
3. Check uploads, PostgreSQL, logs, container layers, and Scylla separately.
4. Never delete PostgreSQL or Scylla database files by hand.
5. Expand storage or use database-supported retention/cleanup mechanisms.
6. Confirm free space and database health before restarting everything.

## TURN failure

Impact: users on restrictive NAT/firewall networks may fail to establish or maintain calls while users with direct peer connectivity still work.

1. Check TURN credentials can be issued.
2. Test relay-only ICE from two unrelated networks.
3. Check listener ports and relay UDP range.
4. Check certificate expiry for `turns:`.
5. Check provider quota/billing or coturn host bandwidth.
6. Restore normal `PLAINWIRE_ICE_TRANSPORT_POLICY=all` after diagnostics.

## Reverse proxy or TLS failure

1. Check certificate status and DNS.
2. Validate proxy configuration before reload.
3. Confirm backend health directly from the proxy host.
4. Confirm WebSocket upgrade behavior.
5. Check upload-body limits separately from ordinary requests.

## Suspected credential leak

1. Determine which secret was exposed.
2. Revoke/rotate it at the source.
3. Update Plainwire configuration through the normal secret path.
4. Restart only the components that need the new credential.
5. Search logs and audit trails for suspicious use.
6. Rotate related secrets when trust boundaries overlap.
7. Document the incident and prevent recurrence.
