# Contributing

Keep this repository practical. Every instruction should answer one of four questions: what to do, why it matters, how to verify it, and how to undo it.

## Rules

1. Test commands before documenting them.
2. Do not commit passwords, API tokens, database dumps, TLS private keys, or production `.env` files.
3. Mark destructive commands clearly.
4. Prefer upstream documentation for changing facts such as supported versions and provider behavior.
5. Keep examples conservative. PostgreSQL is the default message backend. Redis is optional. Scylla is an explicit migration.
6. Do not describe a health check as proof of data correctness.
7. Use plain punctuation. This repository intentionally avoids em dashes.
8. Run `make check` before submitting changes.

## Updating for a new Plainwire version

Run:

```sh
python3 scripts/compare-upstream-env.py /path/to/Plainwire
python3 scripts/rebuild-env-reference.py /path/to/Plainwire
```

Then review the upstream `.env.example`, release notes, storage docs, deployment files, and any new database migrations. Update `docs/reference/upstream-compatibility.md` with the date and source version you checked.
