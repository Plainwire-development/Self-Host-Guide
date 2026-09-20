# Native systemd deployment

A native relx release works well when you do not want the application itself in Docker.

## Layout

Recommended paths:

```text
/opt/plainwire/releases/2.2.0/
/opt/plainwire/current -> /opt/plainwire/releases/2.2.0
/etc/plainwire/plainwire.env
/var/lib/plainwire/uploads/
/var/lib/plainwire/admin-instance.key
/var/log/plainwire/
```

Create a dedicated service account with no interactive login.

## Install

Copy the built release into a versioned directory, then copy [the systemd example](../../examples/systemd/plainwire.service) to `/etc/systemd/system/plainwire.service`.

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now plainwire
sudo journalctl -u plainwire -n 100 --no-pager
```

## Permissions

The runtime user needs write access only where required:

- upload directory;
- admin instance secret directory;
- log/crash dump location when file logging is used.

Keep release binaries administrator-owned and read-only to the service user.

## Upgrade

Install the new release beside the old release, stop Plainwire, switch the `current` symlink, and start. Keep the old release until health checks and smoke tests pass.

A code rollback does not roll back database migrations. Review migration compatibility before switching back.
