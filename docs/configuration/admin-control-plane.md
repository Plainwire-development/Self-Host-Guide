# Host admin control plane

Plainwire has an optional host-level operator console. It manages the Plainwire instance itself, not individual community/server moderation.

## Safe default

```ini
PLAINWIRE_ADMIN_ENABLED=false
PLAINWIRE_ADMIN_BIND=127.0.0.1
PLAINWIRE_ADMIN_PORT=8090
```

Enable it only when you have an operator access plan.

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

Persist and protect this file. It binds operator verification material to the instance.

## Recovery mode

`PLAINWIRE_ADMIN_LOCAL_RECOVERY=true` is an emergency-only option intended for loopback-bound recovery. Remove it after recovery.

## Separation

Do not give ordinary server moderators host-operator access. These are different trust domains.
