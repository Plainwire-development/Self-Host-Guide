#!/bin/sh
set -eu

: "${BACKUP_DIR:?Set BACKUP_DIR}"
: "${PLAINWIRE_ENV_FILE:=/etc/plainwire/plainwire.env}"
: "${PLAINWIRE_UPLOAD_DIR:=/var/lib/plainwire/uploads}"
: "${PGHOST:?Set PGHOST}"
: "${PGUSER:?Set PGUSER}"
: "${PGDATABASE:?Set PGDATABASE}"

STAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="$BACKUP_DIR/$STAMP"
mkdir -p "$OUT"
chmod 700 "$OUT"

pg_dump --format=custom --file="$OUT/postgres.dump" "$PGDATABASE"

if [ -d "$PLAINWIRE_UPLOAD_DIR" ]; then
  tar -C "$PLAINWIRE_UPLOAD_DIR" -czf "$OUT/uploads.tar.gz" .
fi

if [ -f "$PLAINWIRE_ENV_FILE" ]; then
  cp "$PLAINWIRE_ENV_FILE" "$OUT/plainwire.env"
  chmod 600 "$OUT/plainwire.env"
fi

printf '%s\n' "$STAMP" > "$OUT/created-at.txt"
sha256sum "$OUT"/* > "$OUT/SHA256SUMS"
printf 'Backup written to %s\n' "$OUT"
printf 'Copy it off-host and test a restore.\n'
