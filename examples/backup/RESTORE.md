# Restore notes

Do not restore over a running production system as your first test.

1. Create a clean PostgreSQL database.
2. Restore `postgres.dump` with `pg_restore`.
3. Restore uploads to a fresh durable path.
4. Restore the private Plainwire environment and admin instance secret when applicable.
5. Start Plainwire with public traffic blocked.
6. Verify `/api/health`, account login, messages, uploads, roles, and calls.
7. If Scylla is authoritative, restore Scylla with its supported snapshot/backup tooling before opening traffic.

The example backup script is intentionally small. Large PostgreSQL or Scylla installations need a database-specific backup system rather than a shell script alone.
