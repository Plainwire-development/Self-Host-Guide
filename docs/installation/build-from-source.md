# Build Plainwire from source

Build from a clean source checkout when you need a custom image or native release.

## Toolchain

Plainwire 2.1 requires GNU Make 4.3+, Node.js 20.19+ with 22+ recommended, npm, Python 3.9+, Erlang/OTP 27+, and rebar3.

Native driver requirements for `erlcass`:

```sh
sudo apt-get install build-essential cmake pkg-config git \
  libssl-dev libuv1-dev zlib1g-dev ca-certificates
```

Optional native call-health analysis also requires a C11 compiler and `gfortran`.

## Standard build

```sh
make doctor
make build
make browsers
make check
make release
```

For the native call-health worker:

```sh
make doctor NATIVE=1
make build NATIVE=1
make check NATIVE=1
make release NATIVE=1
```

## What `make check` covers

The upstream build runs syntax and manifest checks, browser UI and RTC regressions, call-health parser tests, and EUnit. These tests do not provision your real PostgreSQL, Redis, Scylla, reverse proxy, or TURN provider. Production validation still matters.

## Cluster build

The optional cluster profile adds Partisan:

```sh
make build PROFILE=cluster
```

Do not select it for a normal single-server installation.

## Reproducibility

Keep `rebar.lock` and `package-lock.json`. The upstream project pins Erlang dependencies and uses locked npm dependencies. Build the runtime on the same OS family and architecture as the deployment target when using a native relx release.
