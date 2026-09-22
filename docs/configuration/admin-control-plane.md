# Host admin control plane

Plainwire has an optional host-level operator console. It manages the Plainwire instance itself, not individual community or server moderation. It does not read message bodies, direct-message text, attachment contents, or email addresses.

There is one account-action route: `POST /api/users/:id/moderation`. There is no second admin API, no password tool, and no control that signs an operator in as another user.

## Safe default

```ini
PLAINWIRE_ADMIN_ENABLED=false
PLAINWIRE_ADMIN_BIND=127.0.0.1
PLAINWIRE_ADMIN_PORT=8090
```

Enable it only when you have an operator access plan. The listener is separate from the public app listener (`PORT`, default 8080).

## First owner

Create a normal Plainwire account first. Bootstrap does not invent a user. It promotes an existing active account.

1. Set `PLAINWIRE_ADMIN_ENABLED=true` and keep the bind on loopback.
2. Restart Plainwire. When `admin_operators` is empty, the log contains one line:

   ```text
   [plainwire:admin] FIRST-RUN bootstrap token (one-time): ...
   ```

3. Open `http://127.0.0.1:8090`. Submit that token with the account username and its normal Plainwire password. The panel posts them to `POST /api/bootstrap` as `bootstrap_code`, `username`, and `password`.
4. The response includes a `verification_key`. Store it outside the log. Later sign-in needs the username, the Plainwire password, and that key. The key is shown once.

`PLAINWIRE_ADMIN_BOOTSTRAP_TOKEN` is only a name that secret sanitization still recognizes. The first-owner flow does not read it.

The bootstrap token works once, and only while no operator exists. After that, an owner enrolls other people with a separate one-time enrollment code. Roles are `viewer`, `operator`, and `owner`. A viewer can open overview and host health. Mutating requests need an operator or owner session, the operator cookie, and the `x-csrf-token` header.

## Account actions

Open Users, search by username or display name, and select the row. The detail shows created, updated, last seen, disabled time, whether an email is on file, whether that email is verified, the active session count, and moderation history. It does not show the email address.

These buttons all post `POST /api/users/:id/moderation`. Each one is written to the operator audit and to that account's action history.

| Button | `action` | What it does |
| --- | --- | --- |
| Suspend | `suspend` | Sets `account_state` to `suspended`. Requires a user-facing reason. Ends Plainwire sessions and control-plane sessions. A correct password does not clear it. An optional expiry restores the account on the next login after that time. |
| Ban | `ban` | Same shape as suspend, with `account_state` `banned`. |
| Disable | `disable` | Operator lock. Requires a reason and sets `account_state` to `disabled`. A correct password does not turn it back on. |
| Restore access | `restore` | Sets the account back to `active` and clears the operator reason. Current sessions end; the person signs in again. |
| Sign out everywhere | `revoke_sessions` | Deletes that account's Plainwire sessions and control-plane sessions. `account_state` stays as it was. Connected clients are told `sessions_revoked`. |
| Reset display name | `clear_display_name` | Sets `display_name` to the username. The username and password stay as they were. |
| Remove email | `remove_email` | Clears the address and outstanding verification tokens. The panel still does not show the address. |
| Resend verification | `resend_verification` | Queues a verification message only when mail is enabled on this host. |

Disable is separate from someone disabling their own account. A self-disable stores no operator reason, and the next correct password sets the account back to `active`. An operator disable stores a reason, and that password does not clear it. Restore does.

Resend verification runs only when `pw_mail` is enabled (`PLAINWIRE_MAIL_ENABLED` and SMTP, or the official `plainwi.re` host with SMTP configured). It is limited to 4 attempts per account per 10 minutes. The one-time token is not returned to the browser. If the address is already verified, no message is sent. If no address is on file, the action is rejected.

An operator cannot run these actions on their own account, on another operator, or on an owner. An owner cannot run them on another owner. A viewer cannot post the route.

## Capacity and listener controls

The admin plane has its own listener limits so it does not inherit public-app scale assumptions:

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

Those are the source defaults. The admin plane should remain low-volume. Do not increase these limits just because the public listener is sized for more connections.

## Remote access

The safest remote pattern is to keep the admin listener private and put a dedicated HTTPS origin in front of it:

```ini
PLAINWIRE_ADMIN_ENABLED=true
PLAINWIRE_ADMIN_BIND=127.0.0.1
PLAINWIRE_ADMIN_ALLOW_REMOTE=true
PLAINWIRE_ADMIN_PUBLIC_URL=https://control.example.com
PLAINWIRE_ADMIN_COOKIE_SECURE=true
```

A production bind that is not loopback refuses to start unless `PLAINWIRE_ADMIN_ALLOW_REMOTE=true`, `PLAINWIRE_ADMIN_PUBLIC_URL` is an `https://` URL, and admin cookies are secure. Protect the control hostname with network policy, identity-aware access, VPN, or another operator boundary. Do not expose 8090 directly to the internet.

## Instance secret

Production defaults to:

```text
/var/lib/plainwire/admin-instance.key
```

Override the path with `PLAINWIRE_ADMIN_SECRET_FILE`. In production the path must be absolute. The file is created on first start, mode `0600`, and it binds operator verification material to this instance. Cloning the source tree does not copy a working key. Persist, back up, and restore it with PostgreSQL. Losing the last owner key can only be recovered by someone who can restart that host.

## Recovery mode

`PLAINWIRE_ADMIN_LOCAL_RECOVERY=true` prints a one-time recovery token and is refused when the admin bind is not loopback. It revokes existing admin sessions. Remove the setting after recovery.

## Separation

Do not give ordinary server moderators host-operator access. Instance moderation and host operation are different trust domains.
