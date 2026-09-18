# Operating system packages

Plainwire is easiest to operate on a maintained 64-bit Linux distribution. The runtime is portable, but package names and service management differ by distribution.

The build host needs more than Erlang and Node. Plainwire 2.0 includes `erlcass`, which builds the Cassandra/Scylla C++ driver as native code even when Scylla is disabled at runtime.

## Debian and Ubuntu builder

Install the language toolchains plus the native driver dependencies:

```sh
sudo apt-get update
sudo apt-get install -y \
  git ca-certificates curl make build-essential cmake pkg-config \
  libssl-dev libuv1-dev zlib1g-dev \
  erlang rebar3 nodejs npm python3
```

Verify versions after installation. Distribution repositories do not always carry a new enough Node.js or Erlang release for Plainwire 2.0. The upstream requirements are Node.js 20.19 or newer, with Node 22 or newer recommended, and Erlang/OTP 27 or newer.

For the optional native call-health helper, also install:

```sh
sudo apt-get install -y gfortran
```

## Fedora and RHEL-family builder

Package names vary by release. The equivalent dependency set is:

```text
git
ca-certificates
curl
make
gcc
gcc-c++
cmake
pkgconf-pkg-config
openssl-devel
libuv-devel
zlib-devel
Erlang/OTP 27+
rebar3
Node.js 20.19+
npm
Python 3.9+
```

Use the distribution package manager for the native libraries, then use an appropriate maintained Node/Erlang source when the base repository is too old.

## Void Linux

Void's current repositories carry modern Erlang and Node.js releases, plus the native development libraries Plainwire needs. On a glibc Void host, the package set is approximately:

```sh
sudo xbps-install -S \
  base-devel cmake pkg-config git ca-certificates curl \
  openssl-devel libuv-devel zlib-devel \
  erlang rebar3 nodejs python3
```

Run `node --version`, `erl`, and `rebar3 version` afterward. Plainwire 2.0 still requires Node.js 20.19+ and Erlang/OTP 27+ regardless of what a distribution package is named.

Void also ships musl variants. Treat musl like Alpine for native-NIF validation: build and test the exact release before using it as a production baseline. Docker remains the lowest-friction route on a Void host when you want the application build isolated from the host package set.

## Alpine

Alpine can work, but the musl-based environment is a less conservative choice for an Erlang application with native dependencies. Test the exact `erlcass` NIF and release image you intend to ship. For a first production deployment, Debian or Ubuntu is simpler.

## Runtime image

A multi-stage container does not need compilers in the final image. It does need the shared libraries used by the compiled native driver. On a Debian-family runtime, expect packages equivalent to:

```text
ca-certificates
OpenSSL runtime library
libuv runtime library
zlib runtime library
libstdc++ runtime library
```

The exact OpenSSL package name changes by distribution release. Confirm with `ldd` against the built NIF rather than copying a package list blindly.

## Inspect the native dependency

After a successful build, locate the `erlcass` shared object and inspect its runtime dependencies:

```sh
find _build -type f -name '*.so' -path '*erlcass*' -print
ldd /path/to/erlcass_nif.so
```

Every non-system dependency shown by `ldd` must exist in the runtime image.

## Production host packages

A host that runs a prebuilt Plainwire container usually needs only:

- Docker Engine and the Compose plugin, or another supported container runtime;
- a reverse proxy if it is not part of the Compose stack;
- host firewall tooling;
- time synchronization;
- backup tooling;
- monitoring/log shipping appropriate to your environment.

Do not install PostgreSQL, Redis, ScyllaDB, and coturn into the Plainwire application container. Run them as independent services with separate data directories, health checks, lifecycle, and resource controls.
