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

Another member's profile omits their email address. `email` and `email_verified` are returned on the signed-in account only.

A friend request cannot rewrite an accepted or blocked pair back to pending. The insert updates a row only while its status is still `pending`. An accepted pair stays accepted. A blocked pair stays blocked, and the request is rejected.

A failed block lookup fails closed. If the query that checks whether someone is blocked does not succeed, Plainwire treats them as blocked rather than allowed.

## Encryption-key rotation

`PLAINWIRE_ENC_KEY` protects encrypted application data. Back it up separately from the application host. For an intentional rotation, install the new primary key and retain old keys in `PLAINWIRE_ENC_PREVIOUS_KEYS` until content encrypted with them is no longer needed or has been deliberately re-encrypted. Up to four previous keys are supported by the 2.5 source.

A well-formed encrypted value that fails authentication is not returned as plaintext. Values in the `e1:` envelope that do not authenticate under the current key or a retained previous key come back empty. A value that is not in that envelope is left unchanged, so this does not hide ordinary unencrypted text.

Do not remove an old key merely because the new process starts successfully. Test reads of older protected records first.

## Blind-index message search

Plainwire 2.5 uses a keyed blind index for message search rather than storing a second normalized plaintext search-word database. `PLAINWIRE_SEARCH_KEY` may be configured independently or derived from the encryption key.

Changing the search key invalidates the existing index and requires a rebuild. Back up an independent search key just like other application secrets. Blind indexing reduces plaintext exposure but still leaks equality/frequency relationships and is not a cryptographic guarantee against an operator who controls the server and keys.

## Reverse proxy trust

Only enable `PLAINWIRE_TRUST_PROXY` when the backend is reachable only through trusted proxies or the trusted proxy CIDRs are explicit. Keep `PLAINWIRE_TRUSTED_PROXIES` narrow.

## Redis

Keep private, authenticated, and optionally ACL-restricted. Redis is acceleration, not durable authority. Queue shedding during a Redis problem is preferable to allowing an accelerator outage to consume unbounded BEAM memory.

## Scylla

Keep CQL private. Use a runtime role limited to the Plainwire keyspace and a separate schema-migration identity when practical.

## Developer applications, webhooks, and AI

Maintain egress controls. Remote Developer Application and AI endpoints require HTTPS. Keep `PLAINWIRE_APP_ALLOW_LOOPBACK_HTTP=false` in production. Signed interaction receivers must validate the timestamp/signature over the raw request body.

AI API keys, system prompts, durable command arguments, and interaction signing secrets are sensitive. Treat a configured third-party AI endpoint as a data recipient for command text intentionally submitted to it.

## Realtime abuse boundaries

Keep WebSocket connection limits, upgrade rate limits, presence-watch caps, fixed-window rate-state caps, and slow-consumer queue limits finite. Raising all of them together removes the protection they are meant to provide.

## Containers

- use immutable images;
- avoid privileged mode;
- avoid mounting the Docker socket into Plainwire;
- keep databases on private networks;
- set resource limits where they protect the host;
- patch base images and dependencies.

## Backups

Treat backups as production data. Encrypt them and restrict access. Backups are incomplete if they omit the keys needed to decrypt restored data.

## Security maintenance

A feature freeze should not freeze security updates. Track Erlang/OTP, OpenSSL, PostgreSQL, Redis, Scylla, Caddy/nginx, coturn, Plainwire dependencies, and application SDK/provider advisories.
