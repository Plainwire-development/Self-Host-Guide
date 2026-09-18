# Logs and health checks

## Health endpoints

Use at least:

```sh
curl --fail http://127.0.0.1:8080/api/health
curl --fail https://chat.example.com/api/health
curl --fail https://chat.example.com/api/version
```

The local check isolates the app. The public check includes DNS, TLS, reverse proxy, and routing.

## Logs

Docker:

```sh
docker compose logs --tail=200 app
docker compose logs --tail=200 db
docker compose logs --tail=200 redis
```

systemd:

```sh
journalctl -u plainwire -n 200 --no-pager
journalctl -u plainwire -f
```

## What to look for

- repeated supervisor restarts;
- PostgreSQL connection errors;
- Redis reconnect loops;
- Scylla connection/backpressure errors;
- storage outbox backlog;
- webhook timeout spikes;
- TURN credential provider errors;
- upload permission errors.

## Privacy

Operational logs can contain account identifiers, IP addresses, URLs, and metadata. Limit access and retention. Do not intentionally log message bodies or authentication secrets for convenience.
