# Caddy reverse proxy

Caddy is a good default reverse proxy for Plainwire because automatic HTTPS and WebSocket proxying require little configuration.

## Minimal production config

See [examples/caddy/Caddyfile](../../examples/caddy/Caddyfile).

The important behavior is:

- public hostname terminates TLS;
- `/api/uploads` gets the larger configured request body allowance;
- ordinary requests get a smaller limit;
- traffic proxies to Plainwire on a private address;
- the backend port is not directly exposed.

## Plainwire settings

```ini
PLAINWIRE_PUBLIC_URL=https://chat.example.com
COOKIE_SECURE=true
PLAINWIRE_TRUST_PROXY=true
PLAINWIRE_TRUSTED_PROXIES=127.0.0.1/32,::1/128
```

If Caddy is in another container or another host, use the proxy network CIDR instead of pretending it is loopback.

## Validate before reload

```sh
caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Then:

```sh
curl -I https://chat.example.com/
curl --fail https://chat.example.com/api/health
```

Caddy's automatic HTTPS requires the public DNS name to resolve to the server and ports 80/443 to be reachable during certificate issuance unless you use another ACME challenge method.
