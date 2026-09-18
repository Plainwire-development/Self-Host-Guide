# Troubleshooting

## Docker build fails with `cmake: command not found`

Plainwire 2.0 builds `erlcass`. Add CMake and native dependencies to the builder stage:

```sh
build-essential cmake pkg-config git ca-certificates libssl-dev libuv1-dev zlib1g-dev
```

Scylla itself does not need to be running for the driver to compile.

## Plainwire boots but Redis appears unused

Check:

```sh
docker compose ps redis
grep '^PLAINWIRE_REDIS_ENABLED=' plainwire.env
docker compose logs app | grep -i redis
```

Redis is optional, so the app can boot while Redis is unavailable.

## Messages work but calls fail between networks

Test TURN. Force `PLAINWIRE_ICE_TRANSPORT_POLICY=relay`, verify relay candidates, then restore `all`.

## Same-LAN calls work, remote calls fail

That strongly suggests NAT/TURN/firewall trouble rather than Plainwire messaging trouble.

## Upload returns 413

The reverse proxy body limit is smaller than Plainwire's upload limit. Fix the proxy route limit.

## Public URL works but WebSocket fails

Check reverse-proxy WebSocket support, origin configuration, forwarded headers, and TLS. Verify the backend is not directly exposed with conflicting proxy-trust settings.

## Scylla enabled but messages still use PostgreSQL

`PLAINWIRE_SCYLLA_ENABLED=true` only enables Scylla connectivity. `PLAINWIRE_MESSAGE_BACKEND` decides authority. `postgres` still uses PostgreSQL for messages.

## Scylla migration is behind

Inspect:

```sh
./scripts/storage-migrate status
./scripts/storage-migrate flush-outbox
./scripts/storage-migrate shadow 500
```

Do not switch to `scylla` until backfill and verification are clean.

## Database password changed and app fails

Update the application secret and database role together, then restart. Confirm no stale container/environment file is still being used.
