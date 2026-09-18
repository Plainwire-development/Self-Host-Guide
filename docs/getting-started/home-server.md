# Home servers, NAT, and CGNAT

Plainwire can run at home, but inbound connectivity is the deciding factor.

## Normal home NAT

If your router has a real public IP, forward TCP 80 and 443 to the reverse proxy. If TURN is on the same public IP, also forward TURN listener and relay ports to the TURN host.

Use DHCP reservations or static LAN addresses so forwarding rules do not drift.

## CGNAT

Carrier-grade NAT means your router does not control the public address. Normal port forwarding cannot make the server reachable.

Options:

- rent a small VPS for the public reverse proxy;
- use a tunnel product for Plainwire HTTP/WebSocket traffic;
- use a managed TURN service for calls;
- ask the ISP for a public IPv4 address;
- use working public IPv6 if your clients and firewall setup support it.

A web tunnel does not replace TURN. Cloudflare Tunnel credentials are different from Cloudflare Realtime TURN credentials.

## Dynamic residential IP

Use dynamic DNS or an API-driven DNS updater. Keep TLS and DNS automation independent of your application process.

## Upload and backup bandwidth

Home upstream bandwidth often becomes the first limit. Upload files, remote backups, and TURN relay traffic all consume upstream capacity. Put backup jobs outside peak hours and consider a managed TURN service if calls are important.

## Power and reliability

Use a UPS for the host, router, modem/ONT, and network switch if you want local outages to degrade gracefully. A UPS is not a backup. Keep data copies off the machine and preferably off-site.
