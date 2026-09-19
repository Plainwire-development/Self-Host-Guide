# Upstream compatibility

## Current target

```text
Plainwire: 2.1.0
Handbook verified: 2026-09-19
```

The 2.1 source snapshot used to refresh this handbook includes:

- PostgreSQL as mandatory relational authority and bounded DB lane admission;
- optional Redis realtime acceleration with pooled I/O workers and bounded queues;
- optional Scylla message/event backend with `postgres`, `dual`, and `scylla` modes;
- concurrent realtime indexes with bounded WebSocket backpressure/admission;
- keyed blind-index message search and encryption-key rotation support;
- Bot API v1, Developer Applications, signed interaction endpoints, and optional AI handlers;
- Gun-based outbound HTTP/webhooks with separate application egress policy;
- coturn/static TURN support and direct Cloudflare Realtime TURN integration;
- optional host admin control plane with dedicated listener controls;
- optional Partisan cluster profile with one realtime owner and a bounded event outbox;
- optional native call-health worker;
- synthetic and live HTTP/WebSocket load harnesses.

The handbook intentionally does not claim unsupported multi-owner WebSocket clustering or SFU media. Plainwire 2.1 calls remain full mesh.

## After upgrading Plainwire

Recheck:

1. `.env.example` for new or removed variables;
2. `rebar.config` for build dependencies;
3. `compose.yaml` and `deploy/`;
4. database migrations and storage semantics;
5. bot/app/webhook/API contract changes;
6. release notes and security audit notes;
7. security-sensitive defaults and key formats;
8. minimum toolchain versions;
9. load-harness behavior and capacity assumptions.

Run:

```sh
python3 scripts/compare-upstream-env.py /path/to/new/Plainwire
python3 scripts/rebuild-env-reference.py /path/to/new/Plainwire
```

Review the generated diff rather than assuming every new token is an operator setting.
