# Official sources

Changing operational facts should be verified against upstream documentation.

## Plainwire source snapshot

This handbook was refreshed against a Plainwire 2.1.0 source snapshot on 2026-09-19, including `.env.example`, `deploy/`, build/release configuration, `docs/BUILDING.md`, `docs/REDIS.md`, `docs/SCYLLA.md`, `docs/CLOUDFLARE_TURN.md`, `docs/SCALING.md`, `docs/BOTS.md`, security/audit notes, storage modules, realtime registry/delivery code, RTC configuration, and load-test targets.

Use the exact tagged/release source you deploy as the final authority. A handbook can lag a patch even when its architecture guidance remains useful.

## External references

- Docker Engine: <https://docs.docker.com/engine/install/>
- Docker Compose plugin: <https://docs.docker.com/compose/install/linux/>
- Caddy automatic HTTPS: <https://caddyserver.com/docs/automatic-https>
- Caddy reverse proxy: <https://caddyserver.com/docs/caddyfile/directives/reverse_proxy>
- PostgreSQL version policy: <https://www.postgresql.org/support/versioning/>
- Redis security: <https://redis.io/docs/latest/operate/oss_and_stack/management/security/>
- Redis ACL: <https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/>
- ScyllaDB system requirements: <https://docs.scylladb.com/manual/stable/getting-started/system-requirements.html>
- ScyllaDB system configuration: <https://docs.scylladb.com/manual/stable/getting-started/system-configuration.html>
- Cloudflare Realtime TURN credentials: <https://developers.cloudflare.com/realtime/turn/generate-credentials/>
- Cloudflare TURN analytics: <https://developers.cloudflare.com/realtime/turn/analytics/>
- coturn project: <https://github.com/coturn/coturn>
- Twilio Network Traversal Service: <https://www.twilio.com/docs/stun-turn>
- Metered TURN REST API: <https://www.metered.ca/docs/turn-rest-api/>
- Void Linux Handbook: <https://docs.voidlinux.org/>
- Void Linux package recipes: <https://github.com/void-linux/void-packages>

Provider pricing, supported versions, and service limits change. Verify them before making cost or compatibility decisions.
