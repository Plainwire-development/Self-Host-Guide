# Handbook release 2.5.0-1

This release targets Plainwire 2.5.0 and was refreshed on 2026-09-22.

## Included

- operator handbook in Markdown;
- prebuilt searchable static documentation site;
- production-oriented Docker Compose baseline;
- Plainwire build Dockerfile example with native `erlcass` build dependencies;
- Caddy and nginx examples;
- coturn and managed TURN guidance;
- PostgreSQL, Redis, and ScyllaDB architecture and migration documentation;
- Bot API, Developer Application, signed interaction, webhook, and AI connector operator guidance, including the 2.2 command sync, member pagination, and renewable claim APIs;
- encryption-key rotation and blind-index search-key guidance;
- backup, restore, upgrade, rollback, incident, failure, and disaster-recovery runbooks;
- production environment validator and secret generator;
- source-derived environment and source-token catalog, regenerated against 2.5.0 when the comparison script is run;
- exact upstream 2.2.0 environment, Caddy, and systemd snapshots, kept as the last frozen example set;
- mail, notification, and 2.2-to-2.5 upgrade guides;
- staged release-load validation guidance;
- GitHub Actions verification and Pages publishing workflows.

## Verification performed for this handbook bundle

The documentation repository is checked with:

```text
make check
python3 -m compileall -q scripts tests
bash -n on shell scripts
source environment comparison against Plainwire 2.5.0
source-derived environment catalog regeneration
local static-site link validation
repository-wide em dash and en dash scan
```

Application release validation is intentionally stricter than handbook validation. Before publishing Plainwire itself, require a zero-exit `make check`, a zero-failure EUnit run, real browser/RTC tests, staged synthetic and live load tests, and a soak test appropriate to the host. See [Release and deployment validation](docs/reference/release-validation.md).

## Scope

This repository documents deployment and operation. It does not replace the Plainwire application repository, vendor documentation, a database backup, or a production change-review process. Capacity numbers are test targets, not guarantees for arbitrary hardware.
