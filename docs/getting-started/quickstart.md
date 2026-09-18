# Quick start

This path gets a production-shaped Plainwire installation running without enabling Scylla.

## 1. Prepare a Linux host

Use a current 64-bit Linux distribution. Debian 13, Ubuntu 24.04 LTS or newer, Fedora Server, and similar maintained distributions are reasonable choices. Give the machine a stable public IP or a reliable DNS endpoint.

Recommended small-instance starting point:

```text
4 vCPU
8 GB RAM
80 GB SSD
1 Gbit/s network where available
```

A smaller box can run Plainwire, but storage, builds, uploads, and TURN traffic compete for resources quickly.

## 2. Create DNS

Point a hostname such as `chat.example.com` at the server. If you self-host coturn, create `turn.example.com` too.

## 3. Install Docker Engine and Compose

Follow Docker's distribution-specific installation instructions. Verify:

```sh
docker version
docker compose version
```

Do not expose the Docker daemon over an unauthenticated TCP socket.

## 4. Prepare configuration

Copy `examples/production/plainwire.env.example` to a private deployment directory and replace every `CHANGE_ME` value.

Generate secrets locally:

```sh
scripts/generate-secrets.sh
```

Keep the resulting environment file mode `0600`.

## 5. Start PostgreSQL and Redis

Use `examples/production/compose.yaml` as a reference. It deliberately keeps PostgreSQL and Redis off public host ports.

```sh
docker compose --env-file plainwire.env up -d db redis
```

Wait until both are healthy.

## 6. Run Plainwire

Set `PLAINWIRE_IMAGE` to the image you built from the upstream source, then:

```sh
docker compose --env-file plainwire.env up -d --no-deps app
```

Keep these settings for the first boot:

```ini
PLAINWIRE_REDIS_ENABLED=true
PLAINWIRE_MESSAGE_BACKEND=postgres
PLAINWIRE_SCYLLA_ENABLED=false
```

## 7. Start HTTPS

The included production Compose stack has a Caddy service and matching `Caddyfile`. Set `PLAINWIRE_HOST` to the public hostname, then start it:

```sh
docker compose --env-file plainwire.env up -d caddy
```

If you prefer a host-installed proxy, omit the Caddy service and follow the [Caddy](../installation/caddy.md) or [nginx](../installation/nginx.md) guide instead. Only the reverse proxy should be publicly reachable on the application path.

## 8. Configure TURN

Use either [coturn](../realtime/coturn.md) or [Cloudflare Realtime TURN](../realtime/cloudflare-turn.md). A public chat service with calls should set:

```ini
PLAINWIRE_REQUIRE_TURN=true
```

## 9. Verify

Check the service locally and through the public origin:

```sh
docker compose --env-file plainwire.env exec app curl --fail http://127.0.0.1:8080/api/health
curl --fail https://chat.example.com/api/health
curl --fail https://chat.example.com/api/version
```

Then use two accounts and two different networks to test messages, uploads, calls, screen sharing, reconnect, and session revocation.

## 10. Back up before inviting users

Back up PostgreSQL, the upload directory, and the private environment file. Test a restore into a separate environment before calling the backup plan complete.

Continue with [Production launch checklist](../reference/production-checklist.md).
