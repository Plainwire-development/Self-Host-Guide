# Uploads and storage

Uploads are durable application data and need their own capacity plan.

## Core settings

```ini
PLAINWIRE_UPLOAD_DIR=/var/lib/plainwire/uploads
PLAINWIRE_UPLOAD_MAX_BYTES=262144000
PLAINWIRE_UPLOAD_MAX_FILES=10
PLAINWIRE_UPLOAD_QUOTA_BYTES=1073741824
PLAINWIRE_UPLOAD_RETENTION_DAYS=90
PLAINWIRE_UPLOAD_CONCURRENCY=64
PLAINWIRE_UPLOAD_USER_CONCURRENCY=4
PLAINWIRE_UPLOAD_INFLIGHT_BYTES=1073741824
PLAINWIRE_UPLOAD_USER_INFLIGHT_BYTES=536870912
```

The reverse proxy request limit must be at least as large as Plainwire's configured maximum for the upload route.

## Filesystem

Use a dedicated durable path. Do not place uploads in a container's writable layer.

Monitor:

- free bytes;
- inode usage;
- upload throughput;
- retention cleanup;
- backup size and duration.

## Security

Do not serve the upload directory as a raw public static directory. Let Plainwire enforce attachment access rules.

Restrict filesystem permissions to the Plainwire service account and backup operator.

## Backups

Database metadata and upload bytes must be backed up consistently enough that restored metadata does not point to missing files. For a busy instance, document the acceptable recovery point and coordinate snapshot timing.
