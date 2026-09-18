# Release and deployment validation

Use this list when moving a new Plainwire release into production.

## Source and build

```sh
make doctor
make check
rebar3 eunit
rebar3 release
```

If Docker is the deployment artifact, build from a clean cache periodically so hidden builder state cannot carry the release.

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
- presence works across reconnects/nodes as applicable;
- rate gates still fail safely;
- Redis restart does not take authentication or message storage down.

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
- mute/unmute;
- reconnect;
- screen share;
- test relay-only ICE;
- leave a call open through TURN credential refresh.

## Operational gate

- backup produced successfully;
- restore drill is recent;
- monitoring sees the new release;
- alerts point to a real contact/runbook;
- rollback command/image is known;
- disk and database headroom are adequate;
- logs contain no secrets.
