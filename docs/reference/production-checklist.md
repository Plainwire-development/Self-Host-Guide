# Production launch checklist

## Release gate

- [ ] exact release source/artifact recorded (2.5.0 for this handbook)
- [ ] builder is OTP 27, 28, or 29
- [ ] `make check` exits zero
- [ ] complete EUnit suite has zero failures
- [ ] browser and real RTC/RTP tests pass
- [ ] staged synthetic load passes at intended capacity
- [ ] live HTTP/WebSocket load passes at intended capacity
- [ ] soak test shows stable memory/queues and clean recovery
- [ ] rollback artifact and command are ready

## Host

- [ ] Supported 64-bit Linux
- [ ] Automatic security updates or documented patch process
- [ ] Time synchronization working
- [ ] File-descriptor/process limits sized for expected connections
- [ ] Disk and inode monitoring
- [ ] Off-host backup destination

## Network

- [ ] DNS points to correct public address
- [ ] 80/443 reach reverse proxy
- [ ] backend 8080 is private
- [ ] admin listener is private/restricted
- [ ] PostgreSQL, Redis, Scylla ports are private
- [ ] TURN listener/relay ports are intentional
- [ ] IPv6 tested or AAAA record removed

## Plainwire

- [ ] `PLAINWIRE_ENV=production`
- [ ] correct `PLAINWIRE_PUBLIC_URL`
- [ ] secure cookies enabled
- [ ] encryption key backed up
- [ ] previous encryption keys retained during rotation
- [ ] search key backed up if independently configured
- [ ] registration policy intentional
- [ ] upload limits intentional
- [ ] WebSocket, presence-watch, rate-state, and async queue limits reviewed
- [ ] `/api/health` and `/api/version` work publicly
- [ ] startup log shows pending migrations, including 53 on an older database, applied once
- [ ] mail is either fully configured or explicitly left off

## PostgreSQL

- [ ] dedicated database and role
- [ ] supported release
- [ ] TLS used where required
- [ ] pool/queue/call/statement timeouts reviewed
- [ ] backup succeeds
- [ ] restore tested

## Redis

- [ ] private network only
- [ ] authentication configured
- [ ] app password matches server password
- [ ] worker-pool and bounded queue defaults reviewed
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
- [ ] screen share video and audio tested on supported browser/OS combinations
- [ ] long call survives credential refresh
- [ ] room-size limits match mesh client/network capacity

## Bots, apps, and egress

- [ ] bot tokens treated as secrets
- [ ] app/webhook egress policy reviewed
- [ ] `PLAINWIRE_APP_ALLOW_LOOPBACK_HTTP=false` in production
- [ ] interaction signatures verified by receivers
- [ ] AI connector destinations and data recipients are intentional
- [ ] request/response and worker concurrency limits reviewed

## Security

- [ ] `.env` not in Git
- [ ] private secrets file permissions
- [ ] admin plane private/restricted
- [ ] no database exposed publicly
- [ ] logs checked for secret leakage
- [ ] proxy trust CIDRs narrow
- [ ] dependency/security review completed

## Operations

- [ ] monitoring installed
- [ ] alerts tested
- [ ] queue/drop/eviction metrics have expected baselines
- [ ] rollback documented
- [ ] incident contacts documented
- [ ] backup age monitored
