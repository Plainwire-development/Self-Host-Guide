# FAQ

## Do I need Redis?

No. Plainwire can run without it. Redis is recommended once you want distributed rate gates, shared presence, and hot recent-message caching.

## Do I need Scylla?

No. PostgreSQL-only message storage is fully supported. Scylla is for larger history/event workloads and adds operational complexity.

## Does enabling Scylla move messages automatically?

No. Connectivity and message authority are separate. Migrate through `postgres`, `dual`, verification, then `scylla`.

## Can Redis lose its data?

Plainwire is designed so Redis can be treated as ephemeral. A Redis reset should cause cold caches and rebuilt realtime state, not loss of durable messages or accounts.

## Can I run everything on one PC?

Yes for small installations and testing. A growing public service benefits from separating TURN and eventually databases so one workload cannot starve another.

## Can Cloudflare Tunnel replace TURN?

No. It can help publish HTTP/WebSocket traffic, but TURN is a media relay protocol and uses separate credentials and network behavior.

## Why does the Docker build mention CMake if Scylla is off?

The Erlang release can include the `erlcass` driver, and that driver builds native C/C++ dependencies at image build time. Plainwire 2.5 does not fail the PostgreSQL build when that native compile is skipped. Scylla stays unavailable until the driver is built.

## Do I need mail?

No. Self-hosted password reset and address verification stay off until `PLAINWIRE_MAIL_ENABLED=true` and SMTP is configured. See [Mail](../configuration/mail.md).

## Why did channel notifications get quieter in 2.5?

A normal channel message no longer inserts an inbox row for every member. Mentions still do. Opening a DM, channel, or thread deletes the matching notification. See [Notifications](../operations/notifications.md).

## Which Erlang versions work?

OTP 27, 28, and 29. OTP 29 needs the 2.5 erlcass compile hook. See [Build from source](../installation/build-from-source.md).

## Should I expose Redis or Scylla ports?

No. Keep them on private networks.

## Should I enable relay-only WebRTC permanently?

Usually no. `iceTransportPolicy=all` allows direct paths and TURN fallback. Relay-only is useful for diagnostics or specific privacy/network policy requirements, but increases relay bandwidth.
