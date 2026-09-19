# WebRTC, STUN, TURN, and ICE

Plainwire uses WebRTC for calls and screen sharing. The Plainwire server handles signaling, not the normal media path.

## STUN

STUN helps a browser discover how it appears from the public network. It does not relay media.

Plainwire defaults to a public Google STUN endpoint unless `PLAINWIRE_STUN_URLS` is configured.

## TURN

TURN relays media when direct connectivity fails because of NAT, firewall, enterprise network policy, or other path constraints.

For a public instance, configure TURN and use:

```ini
PLAINWIRE_REQUIRE_TURN=true
```

## ICE policy

Normal mode:

```ini
PLAINWIRE_ICE_TRANSPORT_POLICY=all
```

Use `relay` only for diagnostics or an intentional relay-only deployment:

```ini
PLAINWIRE_ICE_TRANSPORT_POLICY=relay
```

Relay-only mode increases TURN bandwidth and cost.

## Plainwire call topology

Plainwire 2.1 uses a peer mesh for calls. The default voice-room cap is 8 participants and the configured maximum is clamped at 32. Full mesh gets expensive as participant count grows. Do not raise the limit because a config knob exists.

Useful settings:

```ini
PLAINWIRE_VOICE_MAX_PARTICIPANTS=8
PLAINWIRE_VOICE_MAX_SHARES=2
PLAINWIRE_RTC_RECONNECT_GRACE_MS=15000
```

## Production test

A same-LAN call does not validate TURN. Test from two different networks, then force relay-only temporarily and inspect the selected ICE candidate path in browser WebRTC diagnostics.
