# Plainwire 2.1 to 2.2

Plainwire 2.2.0 is an additive minor release centered on the bot platform, with call-control, screen-share audio, clipboard, and layout quality-of-life fixes. It does not require a database migration, new runtime dependency, or new server environment variable.

## What changes

The Bot API v1 adds:

- atomic replacement of up to 100 command definitions with `PUT /api/bot/v1/commands`;
- stable cursor pagination for server members with a maximum page size of 200;
- renewable command claims with bounded 5 to 120 second extensions;
- capability discovery for command sync, paginated members, renewable claims, and their effective limits;
- first-party 2.2 SDK methods in C, C++, Go, Rust, Erlang, Python, and JavaScript;
- bounded command-worker helpers in Go, Python, and JavaScript.

Existing command registration, claim, response, failure, and compatibility message routes remain available. The normal server and channel discovery path no longer constructs the complete member roster, which reduces startup work for bots in large servers.

## Before upgrading

1. Back up PostgreSQL, uploads, configuration, the encryption/search/media keys, and the host-admin instance secret.
2. Keep the 2.1 artifact or image available for rollback.
3. Run the upstream `make check` gate on the exact 2.2.0 source or artifact.
4. Compare the deployment environment with the 2.2.0 snapshot:

   ```sh
   python3 scripts/compare-upstream-env.py /path/to/Plainwire-2.2.0
   ```

   The 2.2.0 source token set matches 2.1.0, so no new variable is required. Preserve existing secrets and measured tuning.

5. If bots are deployed, record their command definitions and ensure custom workers preserve claim tokens as secrets.

## Bot worker rollout

Upgrade the Plainwire server before switching workers to 2.2-only routes. Older Bot API v1 workers continue to operate during a staged rollout.

For new workers:

- feature-detect through `GET /api/bot/v1`;
- deploy command definitions atomically rather than issuing a long sequence of one-command updates;
- page through members rather than expecting one unbounded roster response;
- renew a claim before its current lease expires when a handler may run longer than the lease;
- keep claim and handler concurrency bounded;
- treat bot tokens and claim tokens as secrets and never include them in logs.

Do not repeatedly renew abandoned work. Fail permanently invalid input and allow genuinely interrupted work to return through the existing bounded retry policy.

## Calls and desktop behavior

After the upgrade, test screen sharing from every desktop/browser combination you support. Plainwire requests shareable window or system audio, but the browser, operating system, selected capture surface, and user choice ultimately determine whether an audio track is available. A successful screen-share video track does not prove that audio was granted.

Also verify call-overlay controls at narrow and wide viewport sizes and confirm that editable-field right-click paste uses the browser's native menu.

## Validation

Run the normal smoke test plus:

- bulk command sync with create, update, and stale-command removal;
- member pagination across at least two pages;
- claim renewal followed by response;
- concurrent workers claiming distinct invocations;
- claim-time permission revocation;
- screen share with audio where the platform supports it;
- native context-menu paste in message and settings inputs.

## Rollback

Because 2.2.0 adds no schema migration or required configuration, a code rollback to 2.1 is normally possible after stopping 2.2 workers that depend on the new routes. Keep the same database, encryption keys, search key, media signing key, uploads, and admin-instance secret.

Commands synchronized through 2.2 remain normal command records. A 2.1 server can continue serving them, but workers must stop using member pagination and claim renewal until the server is upgraded again.
