# Restore drills

Restore into a separate environment. Never use the first restore test as an experiment on production.

## Order

1. Provision a clean host/network.
2. Restore private configuration and keys.
3. Restore PostgreSQL.
4. Restore uploads.
5. Restore Scylla if it is authoritative.
6. Start Plainwire with public traffic blocked.
7. Run health checks.
8. Test account login, messages, attachments, roles, and calls.
9. Compare expected counts and recent content.
10. Only then consider traffic cutover.

## PostgreSQL-only recovery

When `PLAINWIRE_MESSAGE_BACKEND=postgres`, PostgreSQL plus uploads and secrets contain the durable application state.

## Scylla-backed recovery

When `PLAINWIRE_MESSAGE_BACKEND=scylla`, PostgreSQL alone is not a complete current message-history backup. Restore the Scylla schema and timeline data together with PostgreSQL recovery metadata.

## Recovery objectives

Document:

- RPO, how much data you can lose;
- RTO, how long recovery may take;
- who has backup credentials;
- where keys are stored;
- how DNS or load balancer cutover works.
