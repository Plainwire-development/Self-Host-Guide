# DNS and networking

## DNS

At minimum, create a record for the public application:

```text
chat.example.com -> public server or load balancer
```

If self-hosting TURN:

```text
turn.example.com -> TURN server public IP
```

Use stable addresses. TURN behind arbitrary HTTP-only proxying does not work because TURN uses its own UDP/TCP/TLS listeners and relay ports.

## Public ports

Typical public edge:

```text
80/tcp    HTTP, usually redirected to HTTPS
443/tcp   HTTPS and WebSocket
```

Self-hosted coturn commonly needs:

```text
3478/udp  TURN/STUN
3478/tcp  TURN/STUN over TCP
5349/tcp  TURN over TLS
49152-65535/udp  relay allocation range, unless narrowed deliberately
```

See [Ports and firewall matrix](../reference/ports.md).

## Private ports

Keep these private unless you have a specific secured network design:

```text
8080 Plainwire application
8090 host admin listener
5432 PostgreSQL
6379 Redis
9042 Scylla CQL
```

## Trusted proxy configuration

Set `PLAINWIRE_TRUST_PROXY=true` only when Plainwire is actually behind a trusted reverse proxy. The default trusted proxy CIDRs are loopback. If the proxy is on another host or container network, set `PLAINWIRE_TRUSTED_PROXIES` explicitly.

Do not expose the backend directly while also trusting arbitrary forwarded headers. IP rate limits and client-address logging depend on this boundary.

## WebSocket origin

`PLAINWIRE_ALLOWED_ORIGINS` can explicitly list allowed origins. If empty, Plainwire uses `PLAINWIRE_PUBLIC_URL`. Keep the public URL accurate and HTTPS in production.

## IPv6

If you publish AAAA records, make sure the service is actually reachable and firewalled correctly over IPv6. A broken AAAA record can create intermittent-looking failures for clients that prefer IPv6.
