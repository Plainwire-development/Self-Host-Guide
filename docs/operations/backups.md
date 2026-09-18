# Backups

A Plainwire backup is not one file.

## Back up

1. PostgreSQL.
2. Upload directory or object storage.
3. Private production environment/configuration.
4. Admin instance secret file if the admin plane is enabled.
5. Scylla snapshots/backups when Scylla is authoritative.
6. Reverse proxy and TURN configuration.

Redis does not need persistence for Plainwire correctness.

## PostgreSQL

For small installations, `pg_dump` is easy to reason about:

```sh
pg_dump --format=custom --file=plainwire.dump "$DATABASE_URL"
```

Larger installations may use physical backups and WAL archiving. Whatever you choose, test restoration.

## Uploads

Use filesystem snapshots, `rsync`, object-storage versioning, or another durable copy strategy. Keep the backup consistent enough with database metadata for your recovery objectives.

## Rotation

A basic policy might keep:

- several daily backups;
- several weekly backups;
- at least one monthly backup;
- an off-site copy.

Choose retention based on your threat model and storage budget.

## Encryption

Backup files often contain everything an attacker wants. Encrypt sensitive backups at rest and control access separately from the production host.

## Verify

A backup job exiting zero is not a restore test. Schedule restore drills.
