# Upstream compatibility

## Current target

```text
Plainwire: 2.5.0
Upstream tag commit: 9d9a558aa335ac9db9df6190eee3477b329db9c4
Handbook verified: 2026-09-22
```

Plainwire 2.5.0 keeps the 2.2 platform and adds:

- OTP 29 builds, with `scripts/compile-erlcass.sh` removing `-s init stop` before the erlcass eval;
- database migration 53, applied on startup with the existing advisory lock;
- operator disable, restore, session revocation, display-name reset, email removal, and verification resend on `POST /api/users/:id/moderation`;
- optional self-hosted mail, off unless `PLAINWIRE_MAIL_ENABLED=true` and SMTP is set;
- call seats registered before `peer_joined`, and `voice_state` / `call_state` kept when realtime delivery sheds load;
- inbox rows for mentions, not for every ordinary channel message.

The 2.2 source snapshot that this handbook still describes in the older upgrade pages includes:

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

Plainwire 2.2.0 did not add a database migration. 2.4.0 adds migration 51, 2.4.1 adds migration 52, and 2.5.0 adds migration 53. Existing Bot API v1 clients remain compatible.

The handbook intentionally does not claim unsupported multi-owner WebSocket clustering or SFU media. Plainwire 2.5 calls remain full mesh.

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
