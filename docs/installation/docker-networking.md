# Docker networking

A good Compose layout separates public traffic from private service traffic.

## Two networks

Use an edge network for the reverse proxy and app, and an internal network for the app and databases:

```text
Internet
   |
Caddy/nginx
   |
 edge network
   |
Plainwire
   |
 backend network
   + PostgreSQL
   + Redis
   + ScyllaDB, when enabled
```

The `backend` network in the included production example is marked `internal: true`. Docker does not route that network directly to the outside world.

## Do not publish database ports

For a single-host Compose deployment, these usually need no host `ports:` entry:

```text
5432 PostgreSQL
6379 Redis
9042 Scylla CQL
```

Plainwire reaches them by Compose service name on the private network.

Publishing a database port just to make local debugging convenient is an easy configuration to forget. Use `docker compose exec`, a private VPN, SSH forwarding, or a temporary loopback-only binding instead.

## Reverse proxy placement

The reverse proxy may run:

1. on the host, forwarding to a loopback-bound Plainwire port;
2. in the same Compose project on the edge network;
3. on another trusted host/private network.

If the reverse proxy is remote, configure `PLAINWIRE_TRUSTED_PROXIES` narrowly and protect backend traffic with a private network or TLS.

## TURN is different

TURN is not ordinary HTTP reverse-proxy traffic. A self-hosted coturn server needs direct UDP/TCP reachability and a relay UDP range. Do not expect a normal HTTP reverse proxy to forward TURN media.

A dedicated public IP or small public VPS is often simpler than placing coturn behind complicated NAT.

## DNS

Typical records:

```text
chat.example.com     -> reverse proxy / Plainwire
control.example.com  -> optional admin reverse proxy
turn.example.com     -> coturn public IP, if self-hosting TURN
```

Keep the database names private. They do not need public DNS.

## Container DNS

Inside Compose, use service names:

```ini
PLAINWIRE_DB_HOST=db
PLAINWIRE_REDIS_HOST=redis
PLAINWIRE_SCYLLA_CONTACT_POINTS=scylla
```

Do not use `127.0.0.1` for another container. Inside the Plainwire container, loopback means the Plainwire container itself.
