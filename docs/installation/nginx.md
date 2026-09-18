# nginx reverse proxy

nginx works well if it is already part of your infrastructure.

See [examples/nginx/plainwire.conf](../../examples/nginx/plainwire.conf).

## Requirements

The proxy must support:

- HTTPS;
- WebSocket upgrade headers;
- long-lived WebSocket connections;
- upload body sizes matching Plainwire;
- forwarded client address headers from a trusted proxy boundary.

## Important settings

Use a generous read timeout for WebSockets and disable buffering where latency matters. Do not expose port 8080 publicly.

If TLS terminates at nginx:

```ini
PLAINWIRE_PUBLIC_URL=https://chat.example.com
COOKIE_SECURE=true
PLAINWIRE_TRUST_PROXY=true
```

Keep `PLAINWIRE_TRUSTED_PROXIES` limited to the actual proxy address or network.

## Upload limits

If `PLAINWIRE_UPLOAD_MAX_BYTES=262144000`, nginx must allow at least the same request size on the upload endpoint. A smaller proxy limit fails before Plainwire sees the request.
