# What you are running

Plainwire 2.5 is a realtime chat server built around Erlang/OTP, Cowboy, PostgreSQL, WebSocket, and WebRTC. PostgreSQL is required. Redis can accelerate short-lived realtime state and stays off until you enable it. ScyllaDB can become the high-volume message timeline after an explicit migration. TURN provides a relay path for calls when direct peer-to-peer connectivity fails.

A normal small installation does not need every optional component. Start with the smallest topology that meets your needs, then add services because measurements justify them.

```text
Internet
   |
   v
Caddy or nginx :443
   |
   v
Plainwire :8080
   |---------------- PostgreSQL :5432    required relational authority
   |---------------- Redis :6379         optional realtime accelerator
   |---------------- ScyllaDB :9042      optional timeline backend
   |
   +---- HTTPS to approved integrations and TURN credential providers

Browsers <---------------- WebRTC ----------------> Browsers
                  \        TURN        /
                   \------ relay ------/
```

## What each component owns

| Component | Responsibility | Can Plainwire run without it? |
| --- | --- | --- |
| Plainwire | API, WebSocket, authorization, message logic, RTC signaling, admin plane | No |
| PostgreSQL | Accounts, servers, channels, membership, roles, permissions, integration config, and default message storage | No |
| Redis | Distributed rate gates, node-aware presence, hot recent-message cache | Yes |
| ScyllaDB | High-volume message timeline and event history when enabled | Yes |
| Reverse proxy | Public TLS termination and HTTP routing | Public deployments should use one |
| TURN | Media relay for difficult NAT and firewall cases | Calls become less reliable without it |

## Storage rule

Keep one authority for each kind of data.

- PostgreSQL is relational truth.
- Redis is disposable acceleration.
- Scylla is ordered history at scale when the message backend is switched.
- Object or filesystem storage holds upload bytes.

If Redis is empty after a restart, Plainwire should recover. If PostgreSQL is lost without a backup, the installation is not recoverable. If Scylla is the active message backend, it becomes part of the backup and recovery plan.

## Safe first deployment

For a first public instance, use PostgreSQL, a reverse proxy, and a TURN service. Leave Redis off until you want shared presence and distributed rate gates. Leave `PLAINWIRE_MESSAGE_BACKEND=postgres` and `PLAINWIRE_SCYLLA_ENABLED=false` until you have a reason to operate Scylla. Existing installs apply pending migrations, including migration 53, when the database process starts.

Next: [Quick start](quickstart.md).
