# Environment variable reference

This is the operator-facing environment reference refreshed against the Plainwire 2.2.0 source snapshot. It intentionally prioritizes variables present in the upstream production example plus a small number of compatibility/build names. The [complete source token catalog](environment-source-catalog.md) records every `PLAINWIRE_*` token found in the source tree.

Do not set every variable. Start from upstream `.env.example`, then add advanced controls only for a measured or architecture-specific reason.

| Variable | Default or note | Type | Audience |
| --- | --- | --- | --- |
| `PLAINWIRE_ADAPTIVE_SCREEN` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_ACCEPTORS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_ALLOW_REMOTE` | false | setting | operator |
| `PLAINWIRE_ADMIN_BIND` | 127.0.0.1 | setting | operator |
| `PLAINWIRE_ADMIN_BOOTSTRAP_TOKEN` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_ADMIN_CONNECTION_SUPERVISORS` | 4 | setting | operator |
| `PLAINWIRE_ADMIN_COOKIE_SECURE` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_ENABLED` | false | setting | operator |
| `PLAINWIRE_ADMIN_ENROLLMENT_MINUTES` | 60 in production example | setting | operator |
| `PLAINWIRE_ADMIN_HANDSHAKE_TIMEOUT_MS` | 5000 | setting | operator |
| `PLAINWIRE_ADMIN_IDLE_TIMEOUT_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_LOCAL_RECOVERY` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_MAX_CONNECTIONS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_MAX_KEEPALIVE` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_PORT` | 8090 | setting | operator |
| `PLAINWIRE_ADMIN_PUBLIC_URL` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_REQUEST_TIMEOUT_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ADMIN_SECRET_FILE` | /var/lib/plainwire/admin-instance.key in production | setting | operator |
| `PLAINWIRE_ADMIN_SEND_TIMEOUT_MS` | 10000 | setting | operator |
| `PLAINWIRE_ADMIN_SESSION_HOURS` | 12 in production example | setting | operator |
| `PLAINWIRE_AI_COMMANDS_PER_APP_PER_MINUTE` | 60 | setting | operator |
| `PLAINWIRE_AI_COMMAND_CONCURRENCY` | 4 | setting | operator |
| `PLAINWIRE_AI_COMMAND_TIMEOUT_MS` | 30000 | setting | operator |
| `PLAINWIRE_ALLOWED_ORIGINS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ALLOW_ARBITRARY_MEDIA` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ALLOW_INSECURE_DB` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ALLOW_STATIC_TURN_CREDENTIALS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_ALLOW_UNSIGNED_MEDIA_TOKENS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_APP_ALLOW_LOOPBACK_HTTP` | false | setting | operator |
| `PLAINWIRE_APP_COMMAND_LEASE_MS` | 45000 | setting | operator |
| `PLAINWIRE_APP_COMMAND_MAX_ATTEMPTS` | 6 | setting | operator |
| `PLAINWIRE_APP_INTERACTION_CONCURRENCY` | 8 | setting | operator |
| `PLAINWIRE_APP_INTERACTION_TIMEOUT_MS` | 10000 | setting | operator |
| `PLAINWIRE_APP_NAME` | Plainwire | setting | operator |
| `PLAINWIRE_APP_REQUEST_MAX_BYTES` | 65536 | setting | operator |
| `PLAINWIRE_APP_RESPONSE_MAX_BYTES` | 131072 | setting | operator |
| `PLAINWIRE_ASSET_VERSION` | see source/defaults for this advanced knob | setting | test/internal |
| `PLAINWIRE_ASYNC_MAX_QUEUE` | 4096 | setting | operator |
| `PLAINWIRE_ASYNC_WORKERS` | 16 | setting | operator |
| `PLAINWIRE_BASE_URL` | SDK example variable, not a server runtime setting | setting | test/internal |
| `PLAINWIRE_BOT_COMMAND_CLAIM_PER_MINUTE` | 2400 | setting | operator |
| `PLAINWIRE_BOT_COMMAND_LEASE_MS` | 30000 | setting | operator |
| `PLAINWIRE_BOT_COMMAND_MAX_ATTEMPTS` | 8 | setting | operator |
| `PLAINWIRE_BOT_MESSAGE_PER_MINUTE` | 300 | setting | operator |
| `PLAINWIRE_BOT_MUTATION_PER_MINUTE` | 600 | setting | operator |
| `PLAINWIRE_BOT_READ_PER_MINUTE` | 1200 | setting | operator |
| `PLAINWIRE_BOT_TOKEN` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_CALL_RING_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_CF_ACCOUNT_ID` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_CF_ANALYTICS_API_TOKEN` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_CF_TURN_API_TOKEN` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_CF_TURN_KEY_ID` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_CF_USAGE_CHECK_INTERVAL_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_CLUSTER_DEDUP_LIMIT` | 262144 | setting | operator |
| `PLAINWIRE_CLUSTER_DRAIN_BATCH` | 128 | setting | operator |
| `PLAINWIRE_CLUSTER_EVENT_MAX_AGE_MS` | 12000 | setting | operator |
| `PLAINWIRE_CLUSTER_OUTBOX_LIMIT` | 8192 | setting | operator |
| `PLAINWIRE_CLUSTER_RETRY_MS` | 500 | setting | operator |
| `PLAINWIRE_CLUSTER_REVALIDATE_JITTER_MS` | 10000 | setting | operator |
| `PLAINWIRE_COMPRESS_OVERSIZE_UPLOADS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_DB_CALL_TIMEOUT_MS` | 60000 | setting | operator |
| `PLAINWIRE_DB_HOST` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_DB_IDLE_TX_TIMEOUT_MS` | 15000 | setting | operator |
| `PLAINWIRE_DB_LOCK_TIMEOUT_MS` | 5000 | setting | operator |
| `PLAINWIRE_DB_MAX_QUEUE` | 250 | setting | operator |
| `PLAINWIRE_DB_NAME` | plainwire | setting | operator |
| `PLAINWIRE_DB_PASS` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_DB_POOL_SIZE` | 10 in code, 20 in production example | setting | operator |
| `PLAINWIRE_DB_PORT` | 5432 | setting | operator |
| `PLAINWIRE_DB_SLOW_MS` | 250 | setting | operator |
| `PLAINWIRE_DB_SSL` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_DB_STATEMENT_TIMEOUT_MS` | 15000 | setting | operator |
| `PLAINWIRE_DB_USER` | plainwire | setting | operator |
| `PLAINWIRE_DEFAULT_THEME` | system | setting | operator |
| `PLAINWIRE_DEVELOPER_APP_LIMIT` | 25 | setting | operator |
| `PLAINWIRE_ENC_KEY` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_ENC_PREVIOUS_KEYS` | empty by default | secret | operator |
| `PLAINWIRE_ENV` | production in the production example | setting | operator |
| `PLAINWIRE_FILE_REQUESTS_PER_MINUTE` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_GITHUB_CACHE_TTL_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_GITHUB_TOKEN` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_HOST` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_HTTP_ACCEPTORS` | 100 | setting | operator |
| `PLAINWIRE_HTTP_CONNECTION_SUPERVISORS` | 8 | setting | operator |
| `PLAINWIRE_HTTP_CONNECT_TIMEOUT_MS` | 2500 | setting | operator |
| `PLAINWIRE_HTTP_FETCH_TIMEOUT_MS` | 8000 | setting | operator |
| `PLAINWIRE_HTTP_HANDSHAKE_TIMEOUT_MS` | 5000 | setting | operator |
| `PLAINWIRE_HTTP_IDLE_TIMEOUT_MS` | 60000 | setting | operator |
| `PLAINWIRE_HTTP_MAX_CONNECTIONS` | 100000 | setting | operator |
| `PLAINWIRE_HTTP_MAX_KEEPALIVE` | 1000 | setting | operator |
| `PLAINWIRE_HTTP_REQUEST_TIMEOUT_MS` | 30000 | setting | operator |
| `PLAINWIRE_HTTP_SEND_TIMEOUT_MS` | 15000 | setting | operator |
| `PLAINWIRE_ICE_TRANSPORT_POLICY` | all | setting | operator |
| `PLAINWIRE_IDLE_TIMEOUT_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_INSTANCE_DESCRIPTION` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_INSTANCE_ID` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_KLIPY_API_KEY` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_KLIPY_CONTENT_FILTER` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_KLIPY_COUNTRY` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_KLIPY_LOCALE` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_KRISP_ENABLED` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_MAX_SESSIONS_PER_USER` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_MEDIA_ALLOWED_HOSTS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_MEDIA_FETCH_CONCURRENCY` | 24 | setting | operator |
| `PLAINWIRE_MEDIA_QUALITY` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_MEDIA_QUALITY_BIN` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_MEDIA_REQUESTS_PER_MINUTE` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_MEDIA_SIGNING_KEY` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_MESSAGE_BACKEND` | postgres | setting | operator |
| `PLAINWIRE_MESSAGE_ID_CLOCK_ROLLBACK_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_MESSAGE_NODE_ID` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_NODE_ID` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_PBKDF2_ITERS` | 160000 | setting | operator |
| `PLAINWIRE_PRESENCE_WATCH_MAX` | 2000 | setting | operator |
| `PLAINWIRE_PROFILE_IMAGE_MAX_BYTES` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_PUBLIC_URL` | required public origin | setting | operator |
| `PLAINWIRE_RATE_MAX_ENTRIES` | 500000 | setting | operator |
| `PLAINWIRE_REDIS_ASYNC_QUEUE` | 4096 | setting | operator |
| `PLAINWIRE_REDIS_DB` | 0 | setting | operator |
| `PLAINWIRE_REDIS_ENABLED` | false | setting | operator |
| `PLAINWIRE_REDIS_HOST` | 127.0.0.1 | setting | operator |
| `PLAINWIRE_REDIS_PASSWORD` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_REDIS_POOL_SIZE` | 8 | setting | operator |
| `PLAINWIRE_REDIS_PORT` | 6379 | setting | operator |
| `PLAINWIRE_REDIS_PREFIX` | plainwire | setting | operator |
| `PLAINWIRE_REDIS_SYNC_QUEUE` | 2048 | setting | operator |
| `PLAINWIRE_REDIS_TIMEOUT_MS` | 80 | setting | operator |
| `PLAINWIRE_REDIS_TLS` | false | setting | operator |
| `PLAINWIRE_REDIS_TLS_INSECURE` | false | setting | operator |
| `PLAINWIRE_REDIS_USERNAME` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_REGISTRATION_ENABLED` | true | setting | operator |
| `PLAINWIRE_RELEASE_BIN` | see source/defaults for this advanced knob | setting | test/internal |
| `PLAINWIRE_REQUIRE_TURN` | true by default in production validation | setting | operator |
| `PLAINWIRE_RTC_RECONNECT_GRACE_MS` | 15000 in production example | setting | operator |
| `PLAINWIRE_SCYLLA_BACKFILL_BATCH` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_BACKFILL_CONCURRENCY` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_BACKFILL_MAX_ROWS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_BUCKET_POLICY` | month | setting | operator |
| `PLAINWIRE_SCYLLA_CACHE_TTL_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_CA_FILE` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_CERT_FILE` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_CONNECT_TIMEOUT_MS` | 5000 | setting | operator |
| `PLAINWIRE_SCYLLA_CONSISTENCY` | local_quorum | setting | operator |
| `PLAINWIRE_SCYLLA_CONTACT_POINTS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_DELIVERY_RETENTION_DAYS` | 90 | setting | operator |
| `PLAINWIRE_SCYLLA_DRIVER_QUEUE` | 32768 | setting | operator |
| `PLAINWIRE_SCYLLA_ENABLED` | false | setting | operator |
| `PLAINWIRE_SCYLLA_EVENT_RETENTION_DAYS` | 365 | setting | operator |
| `PLAINWIRE_SCYLLA_HISTORY_BUCKETS` | 36 in production example | setting | operator |
| `PLAINWIRE_SCYLLA_IO_THREADS` | 2 | setting | operator |
| `PLAINWIRE_SCYLLA_KEYSPACE` | plainwire | setting | operator |
| `PLAINWIRE_SCYLLA_KEY_FILE` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_SCYLLA_LOCAL_DC` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_MAX_INFLIGHT` | 256 | setting | operator |
| `PLAINWIRE_SCYLLA_MAX_PAGE_SCAN_ROWS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_MAX_PARTITION_INFLIGHT` | 8 | setting | operator |
| `PLAINWIRE_SCYLLA_MAX_PARTITION_QUEUE` | 128 | setting | operator |
| `PLAINWIRE_SCYLLA_MAX_QUEUE` | 4096 | setting | operator |
| `PLAINWIRE_SCYLLA_MIGRATION_MODE` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_OPERATION_TIMEOUT_MS` | 8000 | setting | operator |
| `PLAINWIRE_SCYLLA_PARITY_SAMPLE_ROWS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_PASSWORD` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_SCYLLA_POOL_SIZE` | 2 | setting | operator |
| `PLAINWIRE_SCYLLA_PORT` | 9042 | setting | operator |
| `PLAINWIRE_SCYLLA_RECONCILE_INTERVAL_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_RECONCILE_ROWS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_REPLICATION_FACTOR` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_REQUEST_TIMEOUT_MS` | 5000 | setting | operator |
| `PLAINWIRE_SCYLLA_SHADOW_SAMPLE_ROWS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_TLS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_USERNAME` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_VERIFY_AFTER_ID` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_VERIFY_LIMIT` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_WRITE_INTENT_BUCKETS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_WRITE_INTENT_GRACE_MS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SCYLLA_WRITE_INTENT_RECONCILE_ROWS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SEARCH_BACKFILL_BATCH` | 100 | setting | operator |
| `PLAINWIRE_SEARCH_BACKFILL_INTERVAL_MS` | 1500 | setting | operator |
| `PLAINWIRE_SEARCH_KEY` | empty by default | secret | operator |
| `PLAINWIRE_SESSION_DAYS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_SOURCE_REPOSITORY` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_STORAGE_OUTBOX_BATCH` | 25 | setting | operator |
| `PLAINWIRE_STORAGE_OUTBOX_CONCURRENCY` | 8 | setting | operator |
| `PLAINWIRE_STORAGE_OUTBOX_FAILED_RETENTION_DAYS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_STORAGE_OUTBOX_INTERVAL_MS` | 250 | setting | operator |
| `PLAINWIRE_STORAGE_OUTBOX_RETENTION_DAYS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_STUN_URLS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_TEST_BOOL` | see source/defaults for this advanced knob | setting | test/internal |
| `PLAINWIRE_TEST_NATIVE` | see source/defaults for this advanced knob | setting | test/internal |
| `PLAINWIRE_TRUSTED_PROXIES` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_TRUST_PROXY` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_TURN_CREDENTIAL` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_TURN_MONTHLY_LIMIT_BYTES` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_TURN_SECRET` | see source/defaults for this advanced knob | secret | operator |
| `PLAINWIRE_TURN_TTL_SECONDS` | 3600 | setting | operator |
| `PLAINWIRE_TURN_URLS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_TURN_USERNAME` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_UPLOAD_CONCURRENCY` | 64 | setting | operator |
| `PLAINWIRE_UPLOAD_DIR` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_UPLOAD_IMAGE_MAX_DIMENSION` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_UPLOAD_INFLIGHT_BYTES` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_UPLOAD_MAX_BYTES` | 262144000 | setting | operator |
| `PLAINWIRE_UPLOAD_MAX_FILES` | 10 | setting | operator |
| `PLAINWIRE_UPLOAD_QUOTA_BYTES` | 1073741824 | setting | operator |
| `PLAINWIRE_UPLOAD_RETENTION_DAYS` | 90 | setting | operator |
| `PLAINWIRE_UPLOAD_USER_CONCURRENCY` | 4 | setting | operator |
| `PLAINWIRE_UPLOAD_USER_INFLIGHT_BYTES` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_VOICE_MAX_PARTICIPANTS` | 8 | setting | operator |
| `PLAINWIRE_VOICE_MAX_SHARES` | 2 | setting | operator |
| `PLAINWIRE_WEBHOOK_ALLOW_HTTP` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_WEBHOOK_CONCURRENCY` | 8 | setting | operator |
| `PLAINWIRE_WEBHOOK_DELIVERED_RETENTION_DAYS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_WEBHOOK_FAILED_RETENTION_DAYS` | see source/defaults for this advanced knob | setting | operator |
| `PLAINWIRE_WEBHOOK_TIMEOUT_MS` | 8000 | setting | operator |
| `PLAINWIRE_WEBHOOK_WORKER_TIMEOUT_MS` | 13000 in production example | setting | operator |
| `PLAINWIRE_WS_COMPRESS` | true | setting | operator |
| `PLAINWIRE_WS_HARD_QUEUE` | 2000 | setting | operator |
| `PLAINWIRE_WS_MAX_CONNECTIONS` | 100000 | setting | operator |
| `PLAINWIRE_WS_SOFT_QUEUE` | 500 | setting | operator |
| `PLAINWIRE_WS_TRACE` | false | setting | operator |
| `PLAINWIRE_WS_UPGRADES_GLOBAL_MIN` | 60000 | setting | operator |
| `PLAINWIRE_WS_UPGRADES_PER_IP_MIN` | 1200 | setting | operator |

## Non-`PLAINWIRE_` variables

The production path also uses common variables such as `PORT`, `COOKIE_SECURE`, `NODE_ENV`, and `ERL_FLAGS`.

## Source of truth

When this reference and a newer Plainwire release disagree, the newer release source wins. Run the included upstream comparison script after every upgrade.
