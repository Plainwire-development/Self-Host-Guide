# Requirements

## Runtime requirements

Plainwire 2.2 expects a 64-bit Linux deployment for the normal production path.

Core services:

- PostgreSQL, required;
- HTTPS reverse proxy, required for a public browser deployment;
- durable upload storage;
- TURN for reliable voice and screen sharing across networks.

Optional services:

- Redis for distributed realtime acceleration;
- ScyllaDB for high-volume history;
- native call-health helper;
- optional Partisan cluster profile.

## Build requirements

The upstream 2.0 build documentation requires:

- GNU Make 4.3 or newer;
- Node.js 20.19 or newer, with Node 22 or newer recommended;
- npm;
- Python 3.9 or newer;
- Erlang/OTP 27 or newer;
- rebar3.

`erlcass`, the Scylla/Cassandra driver, builds native code even if Scylla is disabled at runtime. A Linux builder therefore needs the native toolchain. On Debian-family systems install at least:

```sh
apt-get install -y \
  build-essential cmake pkg-config git ca-certificates \
  libssl-dev libuv1-dev zlib1g-dev
```

If you build the optional native call-health worker, also install a C11 compiler, `gfortran`, and the matching runtime library.

## Browser requirements

Plainwire is a browser application. Modern Chromium, Firefox, and Safari-class browsers are the target. Screen capture behavior, shared audio, HDR metadata, and codec behavior differ by browser and operating system. Test the browsers your users actually use.

## Time synchronization

Keep system clocks synchronized. Expiring TURN credentials, TLS, session behavior, database timestamps, and message ID generation all depend on sane clocks. Use chrony, systemd-timesyncd, or another maintained NTP client.

## Filesystem

Use durable SSD-backed storage for PostgreSQL and uploads. Scylla has its own production storage requirements and should not be treated like a lightweight sidecar database.
