# Troubleshooting

## Docker build fails with `cmake: command not found`

Plainwire 2.5 builds `erlcass` when the native toolchain is present. Add CMake and native dependencies to the builder stage if you want the Scylla driver:

```sh
build-essential cmake pkg-config git ca-certificates libssl-dev libuv1-dev zlib1g-dev
```

Scylla itself does not need to be running for the driver to compile. If the native build fails, `scripts/compile-erlcass.sh` exits 0 and PostgreSQL messaging still builds. Scylla stays unavailable until the driver exists.

## OTP 29 compile stops inside erlcass

OTP 29 runs `erl -s init stop` before `-eval`. The stock erlcass Makefile used that order, so the VM stopped before it could write `env.mk`, and the whole release compile aborted. Plainwire 2.5 runs `scripts/compile-erlcass.sh` from the `rebar.config` pre-hook. The script removes `-s init stop`. The expression already ends in `halt()`, which also works on OTP 27 and 28.

Confirm the runtime with:

```sh
erl -eval 'io:format("~s~n",[erlang:system_info(otp_release)]), halt().' -noshell
```

`27`, `28`, and `29` are supported. Do not treat a missing PostgreSQL connection at boot as an OTP failure. The listener can start and then the database process exits with `econnrefused` when Postgres is not running.

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
