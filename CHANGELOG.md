# Changelog

## 2.1.0-1 - 2026-09-19

Updated the handbook for Plainwire 2.1.0.

- retargeted build, deployment, compatibility, and generated-site metadata to 2.1.0;
- regenerated the complete source token catalog against the 2.1.0 source snapshot;
- documented encryption-key rotation, blind-index message search, bounded DB lanes, WebSocket admission/backpressure, async work queues, Redis worker pooling, and bounded cluster outbox behavior;
- expanded Developer Application, Bot API, signed interaction, and AI connector operational guidance;
- added a 2.0 to 2.1 upgrade guide with key/search migration cautions and rollback rules;
- strengthened release validation with full `make check`, EUnit, staged synthetic load, live HTTP/WebSocket load, soak, and WebRTC gates;
- updated production examples with 2.1 capacity, Redis, search, and admin listener controls;
- retained the historical 2.0.0 snapshot examples for operators comparing upgrades.

## 2.0.0-1 - 2026-09-17

Initial Plainwire 2.0 self-hosting handbook.

- complete operator documentation and static documentation website;
- PostgreSQL, Redis, and Scylla responsibility and migration guides;
- WebRTC, coturn, Cloudflare Realtime TURN, and managed TURN guidance;
- production-shaped Docker, Caddy, nginx, systemd, Redis, backup, and Scylla lab examples;
- hardware sizing, networking, security, backup, restore, incident, and disaster-recovery runbooks;
- source-derived catalog covering every `PLAINWIRE_*` token found in the supplied 2.0.0 snapshot;
- configuration validator, secret generator, upstream comparison tool, documentation checks, link tests, and GitHub Pages workflows;
- prebuilt responsive documentation website with local search and dark mode.
