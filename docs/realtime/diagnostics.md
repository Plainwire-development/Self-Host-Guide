# Call and screen-share diagnostics

Call debugging works best when you separate signaling, ICE, media, and browser-capture problems.

## 1. Confirm RTC config

Use Plainwire's connection diagnostics and check that STUN/TURN status is ready. Provider tokens should never appear in browser output.

## 2. Test two networks

Use, for example, home broadband and a phone hotspot. Two clients on the same LAN do not prove TURN works.

## 3. Force TURN temporarily

```ini
PLAINWIRE_ICE_TRANSPORT_POLICY=relay
```

Restart and test. Inspect browser WebRTC internals to confirm a relay candidate pair. Restore `all` when finished.

## 4. Separate microphone and screen problems

Screen capture depends on browser and OS permissions. Shared system/tab audio availability varies by platform. A successful voice call does not prove screen-audio capture is available.

## 5. Watch reconnect behavior

Test:

- brief Wi-Fi loss;
- network change;
- page refresh;
- mute/deafen transitions;
- TURN credential refresh during a long call;
- start/stop/change screen source.

## 6. Use call-health data carefully

Plainwire's optional native call-health worker reports numerical heuristics. It is not a MOS guarantee or a substitute for browser/WebRTC metrics.

## Common causes

- TURN URLs unreachable by firewall;
- bad coturn `external-ip` behind NAT;
- TLS certificate mismatch on `turns:`;
- relay port range blocked;
- provider credential expired;
- browser permission denied;
- corporate network blocks UDP, requiring TCP/TLS relay.
