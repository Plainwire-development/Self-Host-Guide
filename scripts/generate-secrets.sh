#!/bin/sh
set -eu
command -v openssl >/dev/null 2>&1 || { echo "openssl is required" >&2; exit 1; }
printf 'PLAINWIRE_ENC_KEY=%s\n' "$(openssl rand -base64 32 | tr -d '\n')"
printf 'PLAINWIRE_DB_PASS=%s\n' "$(openssl rand -hex 32)"
printf 'PLAINWIRE_REDIS_PASSWORD=%s\n' "$(openssl rand -hex 32)"
printf 'PLAINWIRE_TURN_SECRET=%s\n' "$(openssl rand -hex 32)"
printf 'PLAINWIRE_SCYLLA_PASSWORD=%s\n' "$(openssl rand -hex 32)"
