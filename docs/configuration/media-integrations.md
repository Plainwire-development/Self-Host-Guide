# Optional media integrations

Plainwire can use several optional media and metadata integrations. None are required for core messaging.

## Remote media allowlist

For production, configure trusted remote image/CDN hosts:

```ini
PLAINWIRE_MEDIA_ALLOWED_HOSTS=cdn.example.com,images.example.net
PLAINWIRE_MEDIA_FETCH_CONCURRENCY=24
PLAINWIRE_HTTP_FETCH_TIMEOUT_MS=8000
PLAINWIRE_HTTP_CONNECT_TIMEOUT_MS=2500
```

Avoid `PLAINWIRE_ALLOW_ARBITRARY_MEDIA=true` on a public instance unless you have a deliberate egress security design.

## GitHub source metadata

```ini
PLAINWIRE_SOURCE_REPOSITORY=https://github.com/Plainwire-development/Plainwire
PLAINWIRE_GITHUB_TOKEN=
PLAINWIRE_GITHUB_CACHE_TTL_MS=
```

A token is optional and should have no repository permissions when only public metadata is needed.

## KLIPY

```ini
PLAINWIRE_KLIPY_API_KEY=
PLAINWIRE_KLIPY_CONTENT_FILTER=medium
PLAINWIRE_KLIPY_COUNTRY=US
PLAINWIRE_KLIPY_LOCALE=en_US
```

The key stays on the backend.

## Krisp assets

`PLAINWIRE_KRISP_ENABLED=false` by default. The required licensed assets must exist in the expected private static path before enabling it.

## Native call-health worker

`PLAINWIRE_MEDIA_QUALITY=auto` uses the optional worker when installed. Missing native analysis must not break ordinary calls.
