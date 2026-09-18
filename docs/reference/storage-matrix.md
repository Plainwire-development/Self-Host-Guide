# Storage responsibility matrix

| Data | PostgreSQL | Redis | Scylla | Upload storage |
| --- | --- | --- | --- | --- |
| Accounts | authority | optional cache/gates | no | no |
| Sessions | authority | temporary acceleration | no | no |
| Servers/channels | authority | optional cache | no | no |
| Roles/permissions | authority | optional cache only | no | no |
| Presence | durable identity only | active realtime state | no | no |
| Rate limits | durable account state | distributed ephemeral gate | no | no |
| Messages in `postgres` mode | authority | hot cache | disabled/non-authority | attachments only |
| Messages in `dual` mode | read/write authority | hot cache | mirrored target | attachments only |
| Messages in `scylla` mode | relational recovery mirror | hot cache | timeline authority | attachments only |
| Message lifecycle events | supporting metadata | no | high-volume history | no |
| Audit/delivery history | transactional support | no | high-volume history | no |
| Attachment bytes | metadata/access rules | no | message references | authority for bytes |
| Webhook config | authority | no | no | no |

Rule: caches may accelerate authority, but they must not silently replace it.
