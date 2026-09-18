# Incident response

Write the response plan before the incident.

## First actions

1. Preserve evidence and timestamps.
2. Limit blast radius.
3. Keep known-good backups untouched.
4. Rotate exposed credentials.
5. Avoid destructive cleanup until you know what happened.

## Credential exposure

Rotate only the affected secret when possible:

- database password;
- Redis password;
- Scylla credentials;
- TURN provider token;
- webhook/bot token;
- GitHub/KLIPY token.

Changing `PLAINWIRE_ENC_KEY` is not an ordinary rotation. It can make previously encrypted data unreadable.

## Compromised app host

Assume environment secrets and local admin material may be exposed. Provision a clean host, restore from trusted backups, rotate credentials, and investigate persistence before returning traffic.

## Database incident

Stop destructive automation. Snapshot current state if safe. Decide whether to fail closed, restore, or move to a known-good replica based on the database and incident type.

## Redis incident

Because Redis is non-authoritative, it is usually safe to replace it with a clean instance after fixing the access problem. Expect cold caches and rebuilt presence.

## Scylla divergence

Do not improvise manual row deletion. Return message authority to PostgreSQL if needed, then use Plainwire verification and reconciliation tools.

## Afterward

Write a short post-incident report with timeline, root cause, detection gap, corrective actions, and owners. Add a regression test or monitoring rule where possible.
