# Docker deployment

Docker is the easiest repeatable production path when you control the host.

## Install Docker

Use Docker's official package repository for your distribution. On Debian and Ubuntu, the current package set includes Docker Engine, CLI, containerd, Buildx, and the Compose plugin.

Verify:

```sh
docker version
docker compose version
```

## Build the Plainwire image

Plainwire 2.0 includes `erlcass`, which compiles a native Cassandra/Scylla driver. The builder image must include CMake and native dependencies even if Scylla is disabled at runtime.

Use [Dockerfile.for-upstream-source](../../examples/docker/Dockerfile.for-upstream-source) from the root of an upstream Plainwire source checkout.

The important builder packages are:

```text
build-essential
cmake
pkg-config
git
ca-certificates
libssl-dev
libuv1-dev
zlib1g-dev
```

The runtime stage needs compatible runtime libraries such as OpenSSL, libuv, zlib, and libstdc++.

## Recommended service split

The example production Compose stack starts:

- PostgreSQL;
- Redis;
- Plainwire;
- Caddy for public HTTPS.

Scylla is intentionally not part of the production baseline Compose file. A separate single-node lab file exists for migration rehearsal, while a real production Scylla deployment should use the topology described in the production Scylla guide. coturn is documented separately because many operators put it on another host.

## Do not expose databases

Compose service networking is enough for app-to-database traffic. Avoid host mappings like `0.0.0.0:5432:5432` or `0.0.0.0:6379:6379`.

## Health ordering

A container being `running` does not mean the service is ready. Use health checks for PostgreSQL and Redis, then start Plainwire after they are healthy. The app should still handle temporary Redis failure without taking authentication down.

## Volumes

Persist at least:

```text
PostgreSQL data
Plainwire uploads
Plainwire admin instance secret
Caddy certificate/config state
Scylla data, if enabled on separate Scylla infrastructure
```

Redis should be treated as disposable for Plainwire. Persistence is not required for correctness.

## Deploy pattern

Build an immutable image with a version tag, then change the deployment to the new tag. Do not build production by mutating a running container.

```sh
docker compose --env-file plainwire.env pull
docker compose --env-file plainwire.env up -d db redis
docker compose --env-file plainwire.env up -d --no-deps app
docker compose --env-file plainwire.env up -d caddy
```

Verify health and user flows before removing the prior image.
