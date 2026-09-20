# Upstream compatibility

## Current target

```text
Plainwire: 2.2.0
Upstream tag commit: f12c7bf459d444766a622922f5f5687b1c4dbaf6
Handbook verified: 2026-09-20
```

The 2.2 source snapshot used to refresh this handbook includes:

- PostgreSQL as mandatory relational authority and bounded DB lane admission;
- optional Redis realtime acceleration with pooled I/O workers and bounded queues;
- optional Scylla message/event backend with `postgres`, `dual`, and `scylla` modes;
- concurrent realtime indexes with bounded WebSocket backpressure/admission;
- keyed blind-index message search and encryption-key rotation support;
- Bot API v1 with atomic command-set synchronization, cursor-paginated member reads, and renewable durable-command claims;
- first-party C, C++, Go, Rust, Erlang, Python, and JavaScript bot SDKs, plus bounded command workers in Go, Python, and JavaScript;
- Developer Applications, signed interaction endpoints, and optional AI handlers;
- Gun-based outbound HTTP/webhooks with separate application egress policy;
- coturn/static TURN support and direct Cloudflare Realtime TURN integration;
- optional host admin control plane with dedicated listener controls;
- optional Partisan cluster profile with one realtime owner and a bounded event outbox;
- optional native call-health worker;
- synthetic and live HTTP/WebSocket load harnesses.

Plainwire 2.2.0 does not add a database migration, runtime dependency, or server environment variable. Existing Bot API v1 clients remain compatible; the new bot routes and SDK methods are additive.

The handbook intentionally does not claim unsupported multi-owner WebSocket clustering or SFU media. Plainwire 2.2 calls remain full mesh.

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
