# Build Plainwire from source

Build from a clean source checkout when you need a custom image or native release.

## Toolchain

Plainwire 2.5 requires GNU Make 4.3 or newer, Node.js 20.19 or newer (22 or newer is recommended), npm, Python 3.9 or newer, rebar3, and Erlang/OTP 27, 28, or 29.

Confirm the runtime before compiling:

```sh
erl -eval 'io:format("~s~n",[erlang:system_info(otp_release)]), halt().' -noshell
```

The line should be `27`, `28`, or `29`.

OTP 29 runs `erl -s init stop` before `-eval`. That flag used to abort the erlcass compile hook before any Plainwire beam existed, because the VM stopped before the hook's expression could run. `scripts/compile-erlcass.sh` removes `-s init stop` from the erlcass Makefile and `c_src/nif.mk`. The expression already ends in `halt()`, and that form also works on OTP 27 and 28. Upstream `rebar.config` runs the script as a pre-hook on Linux and macOS before `erlcass` compiles.

A missing Scylla native driver does not fail a PostgreSQL build. If the erlcass sources or the native toolchain are absent, or `make nif_compile` fails, the hook prints a notice and exits 0. Scylla stays unavailable. PostgreSQL messaging still builds.

Install the native toolchain when you want the driver available:

```sh
sudo apt-get install build-essential cmake pkg-config git \
  libssl-dev libuv1-dev zlib1g-dev ca-certificates
```

Optional native call-health analysis also requires a C11 compiler, `gfortran`, and the matching libgfortran runtime on the deployment host.

## Standard build

```sh
make doctor
make build
make browsers
make check
make release
```

`make` alone prints help. `make check` runs syntax and manifest checks, browser UI and RTC regressions, call-health parser tests, and EUnit. These tests do not provision your real PostgreSQL, Redis, Scylla, reverse proxy, or TURN provider. Production validation still matters.

For the native call-health worker:

```sh
make doctor NATIVE=1
make build NATIVE=1
make check NATIVE=1
make release NATIVE=1
```

## Cluster build

The optional cluster profile adds Partisan and needs OTP 27 or newer with OTP sources installed:

```sh
make build PROFILE=cluster
```

Do not select it for a normal single-server installation. The supported topology is still one realtime owner. See [Optional clustering](../operations/clustering.md).

## Reproducibility

Keep `rebar.lock` and `package-lock.json`. The upstream project pins Erlang dependencies and uses locked npm dependencies. Build the runtime on the same OS family and architecture as the deployment target when using a native relx release. `make source` writes a portable source archive. `SOURCE_DATE_EPOCH` sets archive timestamps; otherwise they are zero so identical inputs produce identical source archives.
