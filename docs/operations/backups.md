# Backups

A Plainwire backup is not one file. A restore is only useful if it includes the durable data and every key/configuration item needed to interpret that data.

## Back up

1. PostgreSQL.
2. Upload directory or object storage.
3. Private production environment/configuration.
4. `PLAINWIRE_ENC_KEY` and any active `PLAINWIRE_ENC_PREVIOUS_KEYS`.
5. Independent `PLAINWIRE_SEARCH_KEY` and `PLAINWIRE_MEDIA_SIGNING_KEY` values when configured.
6. Admin instance secret file if the admin plane is enabled.
7. Scylla snapshots/backups when Scylla is authoritative.
8. Reverse proxy and TURN configuration.

Redis persistence is not required for Plainwire correctness. Its contents are disposable acceleration/realtime state.

## PostgreSQL

For small installations, `pg_dump` is easy to reason about:

```sh
pg_dump --format=custom --file=plainwire.dump "$DATABASE_URL"
```

Larger installations may use physical backups and WAL archiving. Whatever you choose, test restoration.

## Uploads

Use filesystem snapshots, `rsync`, object-storage versioning, or another durable copy strategy. Keep the backup consistent enough with database metadata for your recovery objectives.

## Key rotation and backup retention

Do not expire an old encrypted-data backup after discarding the key required to read it unless that loss is intentional. When rotating encryption/search/media keys, update backup documentation and recovery drills at the same time.

## Rotation

A basic policy might keep:

- several daily backups;
- several weekly backups;
- at least one monthly backup;
- an off-site copy.

Choose retention based on recovery objectives, threat model, and storage budget.

## Encryption

Backup files often contain everything an attacker wants. Encrypt sensitive backups at rest and control access separately from the production host. Avoid storing the only copy of backup-decryption material on the same machine as the backups.

## Verify

A backup job exiting zero is not a restore test. Schedule restore drills that prove login, message reads/search, attachments, encrypted integration/application state, and Scylla history where applicable.
