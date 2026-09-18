# Self-hosted coturn

Coturn is the standard self-hosted choice when you want full control over TURN traffic and cost.

## When coturn is a good fit

Use coturn when:

- you control a public IP;
- you can open UDP relay ports;
- you want predictable infrastructure costs;
- you can monitor bandwidth and abuse;
- you are comfortable operating another internet-facing service.

## Plainwire credential model

Plainwire supports coturn's shared-secret REST-style credential model. Configure coturn with `use-auth-secret`, the same `static-auth-secret`, and a realm. Plainwire creates short-lived HMAC credentials from `PLAINWIRE_TURN_SECRET`.

Plainwire:

```ini
PLAINWIRE_TURN_URLS=turn:turn.example.com:3478?transport=udp,turn:turn.example.com:3478?transport=tcp,turns:turn.example.com:5349?transport=tcp
PLAINWIRE_TURN_SECRET=CHANGE_ME_LONG_RANDOM_SECRET
PLAINWIRE_TURN_USERNAME=plainwire
PLAINWIRE_TURN_TTL_SECONDS=3600
PLAINWIRE_REQUIRE_TURN=true
```

Coturn:

```ini
use-auth-secret
static-auth-secret=CHANGE_ME_LONG_RANDOM_SECRET
realm=turn.example.com
```

See [the full coturn example](../../examples/coturn/turnserver.conf).

## Firewall

Common listeners:

```text
3478/udp
3478/tcp
5349/tcp
```

Coturn's default relay range is UDP 49152 through 65535. You can narrow it with `min-port` and `max-port`, but the firewall and coturn config must agree.

## TLS

Use a valid certificate for `turns:`. TURN over TLS helps clients on restrictive networks, but UDP TURN is usually preferable when available.

## Behind NAT

If coturn has a private address behind one-to-one NAT, configure `external-ip` correctly and preserve relay port mappings. A cheap VPS with a direct public IP is simpler.

## Abuse controls

TURN is a bandwidth relay exposed to the internet. Use authentication, quotas/limits, firewall rules, logs, and bandwidth monitoring. Never run an open relay.
