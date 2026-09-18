# Handbook release 2.0.0-1

This release targets Plainwire 2.0.0.

Upstream source archive SHA-256:

```text
24149401932fd16a4d000dedc7be2806cf3e9807fa04b8800a45e4802847a17d
```

## Included

- operator handbook in Markdown;
- prebuilt searchable static documentation site;
- production-oriented Docker Compose baseline;
- Plainwire build Dockerfile example with native `erlcass` build dependencies;
- Caddy and nginx examples;
- coturn and managed TURN guidance;
- PostgreSQL, Redis, and ScyllaDB architecture and migration documentation;
- backup, restore, upgrade, rollback, incident, failure, and disaster-recovery runbooks;
- production environment validator and secret generator;
- source-derived environment-variable catalog;
- GitHub Actions verification and Pages publishing workflows.

## Verification performed

The release was checked with:

```text
make check
python3 -m compileall -q scripts tests
bash -n on shell scripts
YAML parsing on repository YAML files
source environment comparison against Plainwire 2.0.0
source-derived environment catalog determinism check
local static-site link validation
repository-wide em dash and en dash scan
```

At release time, the documentation suite contains 55 handbook pages. The static site is generated from the same navigation manifest used by the repository checks.

## Scope

This repository documents deployment and operation. It does not replace the Plainwire application repository, vendor documentation, a database backup, or a production change-review process.
