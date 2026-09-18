# Plainwire 1.9 to 2.0

Plainwire 2.0 adds Redis and Scylla support, but neither requires a flag-day storage move.

## Safe 2.0 first boot

Keep messages on PostgreSQL:

```ini
PLAINWIRE_MESSAGE_BACKEND=postgres
PLAINWIRE_SCYLLA_ENABLED=false
```

Redis can be enabled after its service and password are configured:

```ini
PLAINWIRE_REDIS_ENABLED=true
```

## Docker build change

2.0 includes `erlcass` in the Erlang release. The Scylla driver compiles native code even when Scylla is disabled at runtime.

If an old 1.9 Dockerfile fails with:

```text
cmake: command not found
Hook for compile failed
```

add CMake and the native driver dependencies to the builder image. See [Docker deployment](../installation/docker.md).

## Do not enable Scylla during the code upgrade

Get 2.0 stable on PostgreSQL first. Then introduce Scylla as a separate change using `postgres -> dual -> scylla` migration stages.

## Redis behavior

Redis is not durable authority. A Redis outage should degrade presence/cache/distributed rate acceleration without invalidating PostgreSQL data.

## Validate old data

After 2.0 is running, test existing accounts, friends, servers, permissions, DMs, channels, uploads, sessions, webhooks, and calls before adding new infrastructure changes.
