# Changelog

## 2.5.0-1 - 2026-09-22

Updated the handbook for Plainwire 2.5.0.

- retargeted the operator pages, site metadata, and upgrade path from 2.2.0 to 2.5.0;
- documented OTP 27 through 29, including the OTP 29 erlcass compile hook;
- documented migration 53 and the operator account actions on the existing moderation route;
- added mail, notification, and 2.2-to-2.5 upgrade pages;
- recorded call seat registration, roster snapshots, outgoing-call names, and call cues;
- tightened the documentation site layout, type, and mobile navigation.

## 2.2.0-1 - 2026-09-20

Updated the handbook for Plainwire 2.2.0.

- retargeted build, deployment, compatibility, and generated-site metadata to 2.2.0;
- documented atomic bot command synchronization, cursor-paginated members, renewable command claims, and the expanded first-party SDK surface;
- added a 2.1 to 2.2 upgrade guide and bot-specific release validation checks;
- regenerated the complete source token catalog and confirmed that 2.2.0 adds no server environment variables;
- added exact 2.2.0 upstream configuration, Caddy, and systemd examples while retaining the 2.1.0 and 2.0.0 snapshots;
- refreshed screen-share audio guidance for browser and operating-system capability limits;
- rebuilt and verified the complete static documentation site.

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
