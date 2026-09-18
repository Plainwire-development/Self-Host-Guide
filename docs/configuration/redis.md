# Redis

Redis is optional, but it is a strong fit for production Plainwire once configured correctly.

## Plainwire uses Redis for

- a second distributed gate on sensitive authentication and operator-login rate limits;
- node-aware short-lived presence;
- hot recent-message windows.

PostgreSQL remains the authority for durable data. Plainwire acknowledges messages only after the durable store accepts them.

## Enable

```ini
PLAINWIRE_REDIS_ENABLED=true
PLAINWIRE_REDIS_HOST=redis
PLAINWIRE_REDIS_PORT=6379
PLAINWIRE_REDIS_PASSWORD=CHANGE_ME
PLAINWIRE_REDIS_DB=0
PLAINWIRE_REDIS_PREFIX=plainwire
PLAINWIRE_REDIS_TIMEOUT_MS=80
```

For multi-node Plainwire, set a stable unique `PLAINWIRE_NODE_ID` on every node.

## Security

Never expose Redis directly to the public internet. Redis protected mode is a safety net, not a network design.

Use:

- private service networking;
- firewall rules;
- authentication;
- Redis ACLs where practical;
- TLS when traffic crosses an untrusted network.

If using ACLs:

```ini
PLAINWIRE_REDIS_USERNAME=plainwire
PLAINWIRE_REDIS_PASSWORD=CHANGE_ME
```

## Persistence

Plainwire treats Redis as ephemeral. You can run it without RDB/AOF persistence because losing Redis state should mean cold caches and rebuilt presence, not durable data loss.

## Failure behavior

Redis failure should degrade acceleration, not make Plainwire unusable. Investigate repeated Redis timeouts, but do not design authentication so Redis is the only protection layer.
