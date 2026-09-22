# Plainwire Self-Hosting Handbook

A deployment and operations handbook for running Plainwire 2.5 on infrastructure you control.

This repository is documentation first. The application source lives in the Plainwire repository. Use this handbook for architecture, deployment, storage, TURN, security, upgrades, backups, recovery, tuning, and day-to-day operations.

> Version target: Plainwire 2.5.0
>
> Handbook verification date: 2026-09-22

## Table of contents

### Start here

- [What you are running](docs/getting-started/overview.md)
- [Quick start](docs/getting-started/quickstart.md)
- [Choose a topology](docs/getting-started/topologies.md)
- [Requirements](docs/getting-started/requirements.md)
- [Hardware and capacity planning](docs/getting-started/hardware-sizing.md)
- [DNS and networking](docs/getting-started/networking.md)
- [Home servers, NAT, and CGNAT](docs/getting-started/home-server.md)

### Installation

- [Docker deployment](docs/installation/docker.md)
- [Operating system packages](docs/installation/os-packages.md)
- [Docker networking](docs/installation/docker-networking.md)
- [Build Plainwire from source](docs/installation/build-from-source.md)
- [Native systemd deployment](docs/installation/systemd.md)
- [Caddy reverse proxy](docs/installation/caddy.md)
- [nginx reverse proxy](docs/installation/nginx.md)

### Configuration

- [Production configuration](docs/configuration/configuration.md)
- [Secrets and keys](docs/configuration/secrets.md)
- [PostgreSQL](docs/configuration/postgresql.md)
- [Redis](docs/configuration/redis.md)
- [ScyllaDB](docs/configuration/scylla.md)
- [Production Scylla design](docs/configuration/scylla-production.md)
- [PostgreSQL to Scylla migration](docs/configuration/scylla-migration.md)
- [Uploads and storage](docs/configuration/uploads.md)
- [Host admin control plane](docs/configuration/admin-control-plane.md)
- [Mail](docs/configuration/mail.md)
- [Webhooks, bots, and outbound traffic](docs/configuration/integrations.md)
- [Optional media integrations](docs/configuration/media-integrations.md)

### Calls and realtime

- [WebRTC, STUN, TURN, and ICE](docs/realtime/webrtc.md)
- [Self-hosted coturn](docs/realtime/coturn.md)
- [Cloudflare Realtime TURN](docs/realtime/cloudflare-turn.md)
- [Other managed TURN providers](docs/realtime/managed-turn.md)
- [Call and screen-share diagnostics](docs/realtime/diagnostics.md)

### Operations

- [Backups](docs/operations/backups.md)
- [Restore drills](docs/operations/restore.md)
- [Upgrades and rollback](docs/operations/upgrades.md)
- [Plainwire 2.2 to 2.5](docs/operations/upgrade-2.2-to-2.5.md)
- [Notifications and unread state](docs/operations/notifications.md)
- [Plainwire 2.1 to 2.2](docs/operations/upgrade-2.1-to-2.2.md)
- [Plainwire 2.0 to 2.1](docs/operations/upgrade-2.0-to-2.1.md)
- [Plainwire 1.9 to 2.0](docs/operations/upgrade-1.9-to-2.0.md)
- [Monitoring and alerting](docs/operations/monitoring.md)
- [Logs and health checks](docs/operations/logs-health.md)
- [Performance tuning](docs/operations/performance.md)
- [Security hardening](docs/operations/security.md)
- [Incident response](docs/operations/incident-response.md)
- [Optional clustering](docs/operations/clustering.md)
- [Troubleshooting](docs/operations/troubleshooting.md)
- [Failure runbooks](docs/operations/runbooks.md)
- [Disaster recovery](docs/operations/disaster-recovery.md)

### Reference

- [Ports and firewall matrix](docs/reference/ports.md)
- [Environment variable reference](docs/reference/environment.md)
- [Complete environment and source token catalog](docs/reference/environment-source-catalog.md)
- [Release and deployment validation](docs/reference/release-validation.md)
- [Command reference](docs/reference/commands.md)
- [Storage responsibility matrix](docs/reference/storage-matrix.md)
- [Production launch checklist](docs/reference/production-checklist.md)
- [FAQ](docs/reference/faq.md)
- [Glossary](docs/reference/glossary.md)
- [Official sources](docs/reference/sources.md)
- [Upstream compatibility](docs/reference/upstream-compatibility.md)
- [Maintaining this handbook](docs/reference/maintaining-handbook.md)

### Ready-to-adapt examples

- [Production Compose stack](examples/production/compose.yaml)
- [Production environment template](examples/production/plainwire.env.example)
- [Plainwire build Dockerfile](examples/docker/Dockerfile.for-upstream-source)
- [Caddyfile](examples/caddy/Caddyfile)
- [nginx config](examples/nginx/plainwire.conf)
- [coturn config](examples/coturn/turnserver.conf)
- [coturn Compose service](examples/coturn/compose.yaml)
- [systemd service](examples/systemd/plainwire.service)
- [Redis config](examples/redis/redis.conf)
- [Backup script](examples/backup/backup.sh)
- [Restore notes](examples/backup/RESTORE.md)
- [Single-node Scylla lab](examples/scylla/lab-compose.yaml)
- [Exact upstream 2.2.0 environment example](examples/upstream-2.2.0/plainwire.env.example)
- [Historical upstream 2.1.0 environment example](examples/upstream-2.1.0/plainwire.env.example)
- [Historical upstream 2.0.0 environment example](examples/upstream-2.0.0/plainwire.env.example)

### Repository tools

- `python3 scripts/check-docs.py` checks links, headings, navigation, and writing rules.
- `python3 scripts/build-site.py` rebuilds the static website.
- `python3 scripts/verify-production-env.py /etc/plainwire/plainwire.env` checks common production mistakes without printing secrets.
- `scripts/generate-secrets.sh` creates strong example secrets locally.
- `python3 scripts/compare-upstream-env.py /path/to/Plainwire` reports configuration variables added or removed upstream.
- `python3 scripts/rebuild-env-reference.py /path/to/Plainwire` rebuilds the complete source-derived configuration catalog after an upstream upgrade.
- `make serve` serves the prebuilt site at `http://127.0.0.1:8000`.


### Repository information

- [Release manifest](RELEASE.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Repository scope and attribution](NOTICE.md)
- [License](LICENSE)

## Documentation website

The complete static site is prebuilt in `site/`. It has no runtime backend, analytics, framework, or CDN requirement. Open `site/index.html`, serve the directory with any static web server, or publish it with Pages, nginx, Caddy, S3-compatible object storage, or another static host.

The design is original. It uses a compact documentation rail, warm accent color, dense reference layout, and responsive content navigation inspired by the clarity of Cloudflare documentation and the straightforward structure of Void Linux documentation.
