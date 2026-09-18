# Production launch checklist

## Host

- [ ] Supported 64-bit Linux
- [ ] Automatic security updates or documented patch process
- [ ] Time synchronization working
- [ ] Disk and inode monitoring
- [ ] Off-host backup destination

## Network

- [ ] DNS points to correct public address
- [ ] 80/443 reach reverse proxy
- [ ] backend 8080 is private
- [ ] PostgreSQL, Redis, Scylla ports are private
- [ ] IPv6 tested or AAAA record removed

## Plainwire

- [ ] `PLAINWIRE_ENV=production`
- [ ] correct `PLAINWIRE_PUBLIC_URL`
- [ ] secure cookies enabled
- [ ] encryption key backed up
- [ ] registration policy intentional
- [ ] upload limits intentional
- [ ] `/api/health` and `/api/version` work publicly

## PostgreSQL

- [ ] dedicated database and role
- [ ] supported release
- [ ] TLS used where required
- [ ] backup succeeds
- [ ] restore tested

## Redis

- [ ] private network only
- [ ] authentication configured
- [ ] app password matches server password
- [ ] outage behavior tested

## Scylla, if enabled

- [ ] production cluster, not development Compose
- [ ] schema migration completed
- [ ] backfill completed
- [ ] outbox caught up
- [ ] shadow/parity verification clean
- [ ] backup/restore documented

## Calls

- [ ] TURN configured
- [ ] two-network call tested
- [ ] relay-only diagnostic tested
- [ ] screen share tested
- [ ] long call survives credential refresh

## Security

- [ ] `.env` not in Git
- [ ] private secrets file permissions
- [ ] admin plane private/restricted
- [ ] no database exposed publicly
- [ ] logs checked for secret leakage
- [ ] dependency/security review completed

## Operations

- [ ] monitoring installed
- [ ] alerts tested
- [ ] rollback documented
- [ ] incident contacts documented
- [ ] backup age monitored
