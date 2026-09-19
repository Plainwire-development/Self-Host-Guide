# Other managed TURN providers

Managed TURN removes the need to operate public relay servers. Provider choice is mostly about regions, bandwidth pricing, API model, observability, and whether Plainwire can consume the credentials safely.

## Practical choices

| Choice | Plainwire fit | Operations | Good when |
| --- | --- | --- | --- |
| Cloudflare Realtime TURN | Native credential integration | Managed | You want the simplest managed path supported directly by Plainwire |
| Self-hosted coturn | Native shared-secret flow | You operate it | You have a public IP, can open UDP relay ports, and want infrastructure control |
| Twilio Network Traversal Service | Server-side temporary-token model, but no dedicated Plainwire adapter yet | Managed | You already use Twilio or are willing to add a credential adapter |
| Metered TURN | Managed TURN with API-driven credentials | Managed | Its regions/pricing/API fit your deployment and you validate credential compatibility |

There is no universal best relay. For the current Plainwire 2.1 code, Cloudflare has the cleanest managed integration and coturn has the cleanest self-hosted integration.

### Cloudflare Realtime TURN

Best fit when you want a managed service with first-class Plainwire integration. Plainwire can generate short-lived credentials through Cloudflare's API without exposing the long-lived token.

### Twilio Network Traversal Service

Twilio provides global STUN/TURN through its Network Traversal Service. Its normal model is server-side token creation. Plainwire does not currently have a dedicated Twilio credential adapter, so using Twilio cleanly may require an integration layer rather than pasting a permanent account secret into client configuration.

### Metered TURN

Metered provides hosted TURN and a credentials API. As with any non-Cloudflare managed provider, verify whether your chosen plan returns credentials that fit Plainwire's static or temporary credential model. Do not expose an account-level secret to browsers.

### Self-hosted coturn

Still the best choice when you want complete control and can operate public UDP infrastructure.

## Static credentials

Plainwire production intentionally does not accept static TURN credentials unless you explicitly allow them:

```ini
PLAINWIRE_ALLOW_STATIC_TURN_CREDENTIALS=true
PLAINWIRE_TURN_USERNAME=...
PLAINWIRE_TURN_CREDENTIAL=...
```

Short-lived credentials are preferable. Treat the static override as a compatibility option, not the default design.

## Provider checklist

Before choosing a provider, verify:

- UDP and TCP/TLS relay endpoints;
- regions close to your users;
- credential TTL and refresh model;
- server-side API authentication;
- bandwidth pricing and alerts;
- abuse controls;
- IPv4/IPv6 behavior;
- status page and support path;
- browser-compatible TURN URLs.
