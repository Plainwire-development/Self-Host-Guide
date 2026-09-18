# Webhooks, bots, and outbound traffic

Plainwire 2.0 includes outbound webhooks and bot APIs. These features create a network egress boundary, so configuration matters.

## Webhooks

Runtime controls include:

```ini
PLAINWIRE_WEBHOOK_TIMEOUT_MS=8000
PLAINWIRE_WEBHOOK_WORKER_TIMEOUT_MS=13000
PLAINWIRE_WEBHOOK_CONCURRENCY=8
PLAINWIRE_WEBHOOK_DELIVERED_RETENTION_DAYS=7
PLAINWIRE_WEBHOOK_FAILED_RETENTION_DAYS=30
```

HTTPS is the normal webhook scheme. `PLAINWIRE_WEBHOOK_ALLOW_HTTP=true` weakens transport security and should be reserved for a controlled private network.

Plainwire applies outbound URL checks intended to reduce SSRF risk. Network-level egress controls are still useful defense in depth.

## Bots

Bots are accounts with one-time credentials and normal server authorization. Roles determine what a bot can read or change. Treat bot tokens like passwords.

## Outbound firewall policy

If you run a restrictive egress firewall, allow only the providers and destinations you actually use. Remember that generic server-created webhooks can target many legitimate HTTPS destinations, so a strict allowlist changes product behavior.

## Secrets

Never return provider secrets to the browser. Plainwire's Cloudflare TURN, GitHub, and KLIPY credentials are server-side configuration.
