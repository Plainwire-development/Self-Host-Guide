# Release and deployment validation

Use this as the promotion gate for a Plainwire 2.1 release. A source tree that merely compiles is not release validated.

## Source and correctness gate

From a clean release candidate:

```sh
make doctor
make check
make release
```

`make check` must exit zero. It should cover source/contract verification, frontend compilation, browser regressions, real RTC/RTP tests, backend compilation, and the complete EUnit suite. Treat any skipped or failed test as an explicit release decision, not a green build.

If native call-health analysis is part of your production artifact, also run the matching `NATIVE=1` build/check path.

## Container checks

- image builds from a clean checkout;
- final image contains required NIF runtime libraries;
- app runs as a non-root user where practical;
- no source secrets are copied into image layers;
- persistent paths are explicit;
- health checks work inside the final image;
- image and service versions are recorded.

For the Scylla driver, inspect the compiled `erlcass` NIF with `ldd` in CI or the builder and verify the matching runtime libraries exist.

## PostgreSQL-only compatibility gate

Before enabling optional infrastructure, boot with:

```ini
PLAINWIRE_MESSAGE_BACKEND=postgres
PLAINWIRE_SCYLLA_ENABLED=false
PLAINWIRE_REDIS_ENABLED=false
```

Verify the baseline application. This proves the new release did not accidentally make an optional service mandatory.

## Redis gate

Enable Redis, then verify:

- authentication succeeds;
- no reconnect loop in logs;
- pooled workers remain healthy under load;
- presence works across reconnects/nodes as applicable;
- rate gates still fail safely;
- Redis restart does not take authentication or message storage down;
- bounded Redis queues recover after a burst instead of growing indefinitely.

## Scylla gate

Do not jump directly to Scylla authority. Follow the migration guide and prove:

- schema migration is explicit and complete;
- driver connectivity is healthy;
- dual mode is stable;
- backfill completes and resumes safely;
- outbox drains;
- verification, shadow reads, and parity checks agree;
- rollback to PostgreSQL has been rehearsed.

## Realtime gate

From two unrelated networks:

- join a voice call;
- mute/unmute and deafen/undeafen;
- reconnect;
- screen share with audio when supported;
- test relay-only ICE;
- leave a call open through TURN credential refresh.

Remember that TURN is a relay, not an SFU. Plainwire 2.1 calls remain full mesh.

## Staged load gate

`make check` is mandatory but does not replace capacity testing. Increase load in stages and stop if latency, memory, database pressure, or queue recovery becomes unhealthy.

Synthetic realtime/control-plane stress:

```sh
make load USERS=100 DURATION=30 RATE=200
make load USERS=1000 DURATION=120 RATE=2500
make load USERS=2500 DURATION=180 RATE=5000
make load USERS=5000 DURATION=300 RATE=10000
```

A 10000-user synthetic run is useful as a future-capacity/stress probe when the host can support it:

```sh
make load-doctor USERS=10000
make load USERS=10000 DURATION=300 RATE=20000
```

Do not require a small self-hosting machine to sustain 10000 users merely because the harness can request it. Release capacity is whatever your measured host can sustain with acceptable latency and recovery.

Live authenticated HTTP/WebSocket load should exercise the real network path in staging:

```sh
make load-live USERS=100 DURATION=60 RATE=0
make load-live USERS=1000 DURATION=120 RATE=0
```

Use the session fixture and `LOAD_BASE_URL` required by the upstream load harness. For large network runs, place the generator on another machine so generator CPU, file descriptors, and ephemeral ports do not become the bottleneck you are measuring.

## Soak and recovery gate

Run a sustained test after burst tests. For example:

```sh
make load USERS=1000 DURATION=3600 RATE=0
```

Watch for:

- memory that never settles after load falls;
- growing BEAM mailboxes or outstanding-delivery reservations;
- DB lane saturation that does not recover;
- Redis queue growth that does not drain;
- stale presence/subscription/RTC ownership entries;
- file-descriptor/socket leakage;
- repeated process restarts.

Also exercise a reconnect storm by disconnecting and reconnecting a large cohort over a short interval. The desired overload behavior is bounded rejection/shedding and recovery, not unbounded queuing.

## Developer application and outbound egress gate

If bots, webhooks, Developer Applications, or AI handlers are enabled:

- verify bot/API scopes and server/channel authorization;
- confirm command claim/retry behavior;
- verify signed interaction endpoints reject invalid signatures/timestamps;
- confirm remote application/AI endpoints require HTTPS;
- leave `PLAINWIRE_APP_ALLOW_LOOPBACK_HTTP=false` in production;
- verify request/response size and concurrency limits;
- confirm AI/API secrets never reach browser responses or logs.

## Key and search gate

- the active `PLAINWIRE_ENC_KEY` is backed up securely;
- previous encryption keys remain available during any intentional rotation;
- a `PLAINWIRE_SEARCH_KEY` change is treated as an index migration;
- restore procedures include every key required to read restored encrypted data.

## Operational gate

- backup produced successfully;
- restore drill is recent;
- monitoring sees the new release;
- alerts point to a real contact/runbook;
- rollback command/image is known;
- disk and database headroom are adequate;
- logs contain no secrets;
- expected queue/drop/eviction counters return to baseline after load.
