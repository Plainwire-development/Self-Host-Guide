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

## 4. Separate microphone, screen video, and screen audio

Screen capture depends on browser and operating-system permissions. Plainwire 2.2 requests window or system audio using the current display-capture constraints, but a browser may still return video without an audio track. A successful voice call or screen video track does not prove screen-audio capture is available.

When screen video works but audio does not:

1. confirm that the selected capture surface is capable of audio sharing on that browser and operating system;
2. enable the browser's share-audio option in the capture picker when it is offered;
3. try a browser tab, window, and full display separately because platforms expose different audio sources for each;
4. inspect the outbound display stream in browser WebRTC diagnostics and confirm it contains a live audio track;
5. test with another participant and avoid judging the result from the sharing client, where echo protection may suppress local playback.

If no audio track is returned, the limitation is in capture capability or permission rather than TURN. TURN relays tracks that already exist; it cannot create missing system audio.

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
- capture picker audio was not enabled or the selected surface cannot expose audio;
- corporate network blocks UDP, requiring TCP/TLS relay.
