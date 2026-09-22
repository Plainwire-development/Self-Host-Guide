# Ports and firewall matrix

| Port | Protocol | Service | Public? | Notes |
| ---: | --- | --- | --- | --- |
| 22 | TCP | SSH | restricted | Prefer VPN, allowlist, or key-only auth |
| 80 | TCP | HTTP | yes | ACME and redirect to HTTPS |
| 443 | TCP | HTTPS/WebSocket | yes | Main Plainwire origin |
| 8080 | TCP | Plainwire backend | no | Reverse proxy target. `PORT` defaults to 8080 |
| 8090 | TCP | Admin plane | no | `PLAINWIRE_ADMIN_PORT`. Loopback unless you proxy it |
| 5432 | TCP | PostgreSQL | no | Private database network |
| 6379 | TCP | Redis | no | Never public |
| 9042 | TCP | Scylla CQL | no | Private database network |
| 3478 | UDP/TCP | TURN/STUN | yes if self-hosted | Standard coturn listener |
| 5349 | TCP | TURN TLS | yes if self-hosted | `turns:` endpoint |
| 49152-65535 | UDP | TURN relay | yes if using default coturn range | Can be narrowed deliberately |

## Example UFW edge rules

For an app host without local TURN:

```sh
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

Restrict SSH further when possible.

For a separate TURN host, add its configured TURN listener and relay range. Do not open database ports simply to make container networking easier.

Mail does not listen. When mail is enabled, Plainwire opens an outbound SMTP connection. The default is TCP 587 with STARTTLS. Port 465 uses implicit TLS. Nothing in Plainwire accepts inbound mail on those ports.
