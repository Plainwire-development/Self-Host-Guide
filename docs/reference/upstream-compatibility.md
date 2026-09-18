# Upstream compatibility

## Current target

```text
Plainwire: 2.0.0
Handbook verified: 2026-09-17
Source archive SHA-256: 24149401932fd16a4d000dedc7be2806cf3e9807fa04b8800a45e4802847a17d
```

The source snapshot used for this handbook includes:

- PostgreSQL as mandatory relational authority;
- optional Redis realtime acceleration;
- optional Scylla message/event backend with `postgres`, `dual`, and `scylla` modes;
- Gun-based outbound HTTP/webhooks;
- coturn/static TURN support;
- direct Cloudflare Realtime TURN integration;
- optional host admin control plane;
- optional Partisan cluster profile;
- optional native call-health worker.

## After upgrading Plainwire

Recheck:

1. `.env.example` for new or removed variables;
2. `rebar.config` for build dependencies;
3. `compose.yaml` and `deploy/`;
4. storage and migration docs;
5. release notes;
6. security-sensitive defaults;
7. minimum toolchain versions.

Run:

```sh
python3 scripts/compare-upstream-env.py /path/to/new/Plainwire
```

This reports configuration names known to the app source that are not in this handbook's snapshot list.
