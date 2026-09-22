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

Plainwire 2.5 uses a peer mesh for calls. The default voice-room cap is 8 participants and the configured maximum is clamped at 32. Full mesh gets expensive as participant count grows. Do not raise the limit because a config knob exists.

Useful settings:

```ini
PLAINWIRE_VOICE_MAX_PARTICIPANTS=8
PLAINWIRE_VOICE_MAX_SHARES=2
PLAINWIRE_RTC_RECONNECT_GRACE_MS=15000
```

## Joining a room

A voice or call seat is registered before other participants are told that someone joined. The hub writes the seat, then sends `voice_peer_joined` or `call_peer_joined`, then sends the roster snapshot (`voice_state` or `call_state`). An offer that races an empty roster is not dropped into a silent pair.

`voice_state` and `call_state` are not discarded when realtime delivery sheds load. Speaking indicators (`voice_activity`, `call_activity`) and presence updates still are. Dropping a roster snapshot is what leaves two peers with no one to connect to until somebody reloads.

## What the caller sees

An outgoing call names the people still being waited on. The waiting line is "Waiting for" those names. The ringing event's profile is the caller, and the client does not use it as the person being called. A named conversation keeps that name as the title. Otherwise the title uses the same people who have not joined yet.

## Client cues

The browser plays a short cue for four call events:

- someone else joins the room you are in;
- someone else leaves;
- you leave;
- someone starts receiving your screen share.

Your own departure does not also play the "someone else left" cue. The screen-share cue fires once per remote viewer when outbound screen video starts flowing to that peer, not on every stats poll.

## Production test

A same-LAN call does not validate TURN. Test from two different networks, then force relay-only temporarily and inspect the selected ICE candidate path in browser WebRTC diagnostics. On the outgoing panel, confirm the waiting line names the other person.
