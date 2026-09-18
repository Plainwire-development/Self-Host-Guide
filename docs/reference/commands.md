# Command reference

## Build

```sh
make doctor
make build
make browsers
make check
make release
```

Native call health:

```sh
make build NATIVE=1
make check NATIVE=1
```

## Docker

```sh
docker compose ps
docker compose logs --tail=200 app
docker compose up -d db redis
docker compose up -d --no-deps app
```

## Health

```sh
curl --fail http://127.0.0.1:8080/api/health
curl --fail https://chat.example.com/api/health
curl --fail https://chat.example.com/api/version
```

## Scylla

```sh
./scripts/scylla-migrate
./scripts/storage-migrate status
./scripts/storage-migrate backfill 50000
./scripts/storage-migrate verify 0 1000
./scripts/storage-migrate shadow 500
./scripts/storage-migrate parity 500
./scripts/storage-migrate reconcile-intents 500
./scripts/storage-migrate reconcile 500
./scripts/storage-migrate flush-outbox
```

## systemd

```sh
systemctl status plainwire
systemctl restart plainwire
journalctl -u plainwire -f
```

## Caddy

```sh
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
```
