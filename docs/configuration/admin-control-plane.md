# Host admin control plane

Plainwire has an optional host-level operator console. It manages the Plainwire instance itself, not individual community/server moderation.

## Safe default

```ini
PLAINWIRE_ADMIN_ENABLED=false
PLAINWIRE_ADMIN_BIND=127.0.0.1
PLAINWIRE_ADMIN_PORT=8090
```

Enable it only when you have an operator access plan.

## Capacity and listener controls

Plainwire 2.2 exposes explicit listener controls so the admin plane cannot accidentally inherit public-app scale assumptions:

```ini
PLAINWIRE_ADMIN_ACCEPTORS=10
PLAINWIRE_ADMIN_CONNECTION_SUPERVISORS=4
PLAINWIRE_ADMIN_MAX_CONNECTIONS=2000
PLAINWIRE_ADMIN_HANDSHAKE_TIMEOUT_MS=5000
PLAINWIRE_ADMIN_SEND_TIMEOUT_MS=10000
PLAINWIRE_ADMIN_IDLE_TIMEOUT_MS=30000
PLAINWIRE_ADMIN_REQUEST_TIMEOUT_MS=15000
PLAINWIRE_ADMIN_MAX_KEEPALIVE=200
```

The admin plane should remain low-volume. Do not increase these limits just because the public listener is sized for more connections.

## Remote access

The safest remote pattern is to keep the admin listener private and put a dedicated HTTPS origin in front of it:

```ini
PLAINWIRE_ADMIN_ENABLED=true
PLAINWIRE_ADMIN_BIND=127.0.0.1
PLAINWIRE_ADMIN_ALLOW_REMOTE=true
PLAINWIRE_ADMIN_PUBLIC_URL=https://control.example.com
PLAINWIRE_ADMIN_COOKIE_SECURE=true
```

Protect the control hostname with network policy, identity-aware access, VPN, or another operator boundary. Do not expose 8090 directly to the internet.

## Instance secret

Production defaults to:

```text
/var/lib/plainwire/admin-instance.key
```

Persist, back up, and protect this file. It binds operator verification material to the instance.

## Recovery mode

`PLAINWIRE_ADMIN_LOCAL_RECOVERY=true` is an emergency-only option intended for loopback-bound recovery. Remove it after recovery.

## Separation

Do not give ordinary server moderators host-operator access. Instance moderation and host operation are different trust domains.
