# Security hardening

Security is a set of boundaries, not a single setting.

## Network

Public:

- reverse proxy on 80/443;
- TURN listener and relay ports if self-hosted.

Private:

- Plainwire backend;
- admin listener;
- PostgreSQL;
- Redis;
- Scylla.

## TLS

Use HTTPS for the public app. Use database/Redis/Scylla TLS when traffic crosses an untrusted network. Do not use insecure TLS verification flags in production.

## Accounts and secrets

- strong unique database passwords;
- private `.env` permissions;
- dedicated database roles;
- separate operator access;
- short-lived TURN credentials;
- rotate provider tokens after suspected exposure.

## Reverse proxy trust

Only enable `PLAINWIRE_TRUST_PROXY` when the backend is reachable only through trusted proxies or the trusted proxy CIDRs are explicit.

## Redis

Keep private, authenticated, and optionally ACL-restricted. Redis documentation explicitly warns against public exposure.

## Scylla

Keep CQL private. Use a runtime role limited to the Plainwire keyspace and a separate schema-migration identity when practical.

## Webhooks and remote media

Maintain egress controls. Plainwire has URL validation, redirect handling, timeouts, and host controls, but network policy is still useful defense in depth.

## Containers

- use immutable images;
- avoid privileged mode;
- avoid mounting the Docker socket into Plainwire;
- keep databases on private networks;
- set resource limits where they protect the host;
- patch base images and dependencies.

## Backups

Treat backups as production data. Encrypt them and restrict access.

## Security maintenance

A feature freeze should not freeze security updates. Track Erlang/OTP, OpenSSL, PostgreSQL, Redis, Scylla, Caddy/nginx, coturn, and Plainwire dependency advisories.
