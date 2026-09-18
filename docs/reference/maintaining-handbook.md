# Maintaining this handbook

This repository is tied to a specific Plainwire release. Treat documentation changes like deployment code: review them, test them, and keep a clear upstream version boundary.

## Update for a new Plainwire release

1. Obtain the new Plainwire source tree from the project's normal release channel.
2. Record the release version and source archive SHA-256 in `UPSTREAM_VERSION` and the compatibility page.
3. Compare environment variables:

   ```sh
   python3 scripts/compare-upstream-env.py /path/to/Plainwire
   ```

4. Rebuild the source-derived environment catalog:

   ```sh
   python3 scripts/rebuild-env-reference.py /path/to/Plainwire
   ```

5. Review every added, removed, or behavior-changing variable by reading the source that consumes it. Do not document a guessed default.
6. Review `rebar.config`, `package.json`, `package-lock.json`, release profiles, database migrations, deployment scripts, and upstream release notes for changed dependencies or operational requirements.
7. Recheck storage behavior, TURN credential handling, proxy trust, upload limits, admin-plane behavior, and health endpoints. These affect production architecture directly.
8. Update examples only after confirming they still match the application behavior.
9. Rebuild and verify the documentation:

   ```sh
   make check
   ```

10. Review the generated `site/` diff before publishing.

## Review external operational guidance

Some recommendations depend on software outside Plainwire. Before a handbook release, recheck the official documentation for:

- supported PostgreSQL releases;
- Redis security and TLS guidance;
- ScyllaDB system requirements and topology guidance;
- coturn listener, relay-port, and authentication behavior;
- Cloudflare Realtime TURN credential behavior;
- managed TURN providers named in the handbook;
- operating-system package names used in installation examples.

Keep vendor-specific claims in the relevant page and list the official source in [Official sources](sources.md).

## Keep examples conservative

The examples should optimize for recoverability and understandable failure modes.

- PostgreSQL stays authoritative unless the Scylla migration has been completed and verified.
- Redis remains disposable acceleration, not the only durable authority.
- Scylla examples marked as lab configurations must not silently become production recommendations.
- Database ports stay private by default.
- Plainwire stays behind an HTTPS reverse proxy.
- TURN credentials are generated or derived on the backend, not embedded in frontend code.
- Compatibility exceptions such as insecure database transport or unsigned media tokens require explicit operator action.

## Documentation rules

The repository intentionally enforces a few writing and structure rules:

- no em dashes or en dashes;
- every navigation page must exist;
- local Markdown links must resolve;
- generated site pages must not retain `.md` links;
- the static site must work without a runtime application server;
- examples must use placeholders rather than live secrets;
- advanced settings should identify whether they are operator-facing, test-only, or build-time tokens.

`scripts/check-docs.py` and the unit tests enforce the mechanical parts of these rules.

## Versioning

`UPSTREAM_VERSION` identifies the Plainwire release this handbook describes. `VERSION` identifies the handbook release. A documentation-only correction can increment the handbook version without changing the upstream target.

When Plainwire behavior changes, update both the affected documentation and the compatibility notes. Do not quietly describe unreleased behavior as if it exists in the target release.

## Publishing the site

The `site/` directory is a complete static build. GitHub Pages can publish it with the included workflow. Any static host can serve the same directory.

Before publication:

```sh
make check
git diff --exit-code -- site
```

The second command is useful in CI after a clean checkout. It catches a committed site that no longer matches the Markdown source or renderer.
