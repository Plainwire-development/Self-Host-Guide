# Cloudflare Realtime TURN

Plainwire 2.5 has direct Cloudflare Realtime TURN credential integration.

## Configure

```ini
PLAINWIRE_CF_TURN_KEY_ID=CHANGE_ME
PLAINWIRE_CF_TURN_API_TOKEN=CHANGE_ME
PLAINWIRE_TURN_TTL_SECONDS=3600
PLAINWIRE_REQUIRE_TURN=true
```

These are Realtime TURN credentials, not Cloudflare Tunnel credentials.

Cloudflare takes priority over the legacy static/coturn settings when both TURN key values are present.

## Why this model is strong

The long-lived provider token stays on the Plainwire backend. Plainwire requests expiring TURN credentials and returns only the short-lived ICE credentials to authenticated clients.

Cloudflare's current TURN documentation recommends generating short-lived credentials server-side and refreshing them during longer WebRTC sessions. Plainwire already has refresh behavior for active calls.

## Optional usage guard

```ini
PLAINWIRE_CF_ACCOUNT_ID=CHANGE_ME
PLAINWIRE_CF_ANALYTICS_API_TOKEN=CHANGE_ME
PLAINWIRE_TURN_MONTHLY_LIMIT_BYTES=950000000000
PLAINWIRE_CF_USAGE_CHECK_INTERVAL_MS=300000
```

This is an issuance guard, not a billing cap. Analytics can be delayed, and already-issued credentials remain usable until expiry.

## Validation

Test a call from two unrelated networks. Then temporarily set:

```ini
PLAINWIRE_ICE_TRANSPORT_POLICY=relay
```

Restart, verify relay candidates are selected, then restore `all`.
