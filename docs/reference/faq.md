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

## Why does the 2.0 Docker build need CMake if Scylla is off?

The Erlang release includes the `erlcass` driver, and that driver builds native C/C++ dependencies at image build time.

## Should I expose Redis or Scylla ports?

No. Keep them on private networks.

## Should I enable relay-only WebRTC permanently?

Usually no. `iceTransportPolicy=all` allows direct paths and TURN fallback. Relay-only is useful for diagnostics or specific privacy/network policy requirements, but increases relay bandwidth.
