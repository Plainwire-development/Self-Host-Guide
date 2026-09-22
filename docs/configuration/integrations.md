# Webhooks, bots, Developer Applications, and outbound traffic

Plainwire 2.5 includes outbound webhooks, Bot API v1, reusable Developer Applications, signed interaction endpoints, and optional AI command handlers. These features create network egress and secret-handling boundaries, so configuration matters.

## Webhooks

Runtime controls include:

```ini
PLAINWIRE_WEBHOOK_TIMEOUT_MS=8000
PLAINWIRE_WEBHOOK_WORKER_TIMEOUT_MS=13000
PLAINWIRE_WEBHOOK_CONCURRENCY=8
PLAINWIRE_WEBHOOK_DELIVERED_RETENTION_DAYS=7
PLAINWIRE_WEBHOOK_FAILED_RETENTION_DAYS=30
```

HTTPS is the normal webhook scheme. `PLAINWIRE_WEBHOOK_ALLOW_HTTP=true` weakens legacy webhook transport security and should be reserved for a controlled private network. It does not enable remote plaintext Developer Application or AI connector traffic.

Plainwire applies outbound URL checks intended to reduce SSRF risk. Network-level egress controls are still useful defense in depth.

## Bots

Bots use scoped credentials and normal server/channel authorization. Treat bot tokens like passwords. Plainwire 2.5 separates rate budgets for reads, message sends, mutations, and durable command claims. Command workers use bounded leases and retries so worker loss does not produce an unbounded delivery loop.

Relevant controls include:

```ini
PLAINWIRE_BOT_READ_PER_MINUTE=1200
PLAINWIRE_BOT_MESSAGE_PER_MINUTE=300
PLAINWIRE_BOT_MUTATION_PER_MINUTE=600
PLAINWIRE_BOT_COMMAND_CLAIM_PER_MINUTE=2400
PLAINWIRE_BOT_COMMAND_LEASE_MS=30000
PLAINWIRE_BOT_COMMAND_MAX_ATTEMPTS=8
```

Redis can coordinate rate state across nodes, but bot authorization remains database-backed.

### Bot deployment and scaling

Use `PUT /api/bot/v1/commands` to atomically synchronize up to 100 desired command definitions. Commands omitted from the request are removed, while a conflict rolls back the complete update. Existing one-command registration remains available for interactive changes.

Fetch large server rosters through `GET /api/bot/v1/members?after=...&limit=...`. Pages are cursor-based and capped at 200 members. Ordinary bot startup and channel discovery no longer load the complete server roster.

Long-running queue handlers should renew a live claim before it expires through `POST /api/bot/v1/commands/claims/:invocation_id/defer`. Extensions are bounded from 5 to 120 seconds and cannot revive an expired, failed, or completed claim. Claim tokens remain one-time secrets whose hashes are stored by Plainwire.

The first-party C, C++, Go, Rust, Erlang, Python, and JavaScript SDKs expose command sync, paginated members, and claim renewal. Go, Python, and JavaScript also provide bounded concurrent command workers with handler maps and automatic response/failure handling. Run more small workers rather than giving one process unbounded concurrency.

Use `GET /api/bot/v1` for capability discovery and effective limits instead of assuming every self-hosted instance has identical tuning. The language-neutral OpenAPI description lives in the upstream `docs/bot-api.openapi.yaml` file.

## Developer Applications

A Developer Application can install a server-scoped bot identity and expose commands through one of three handler styles:

- `queue`, claimed through the versioned Bot API;
- `webhook`, delivered to a signed HTTPS interaction endpoint;
- `ai`, sent to an optional OpenAI-compatible connector.

Installers and invokers are authorization-checked. Plainwire rechecks claim-time access before decrypted command arguments leave the server. Do not broaden bot roles simply to make an integration easier to develop.

### Signed interaction endpoints

Receivers should verify `X-Plainwire-Interaction-Timestamp` and `X-Plainwire-Interaction-Signature` against the raw request body using the application's interaction secret. Reject stale timestamps and invalid signatures before executing a command.

Remote application endpoints require HTTPS. Plain HTTP is allowed only for exact loopback development when explicitly enabled:

```ini
PLAINWIRE_APP_ALLOW_LOOPBACK_HTTP=false
PLAINWIRE_APP_REQUEST_MAX_BYTES=65536
PLAINWIRE_APP_RESPONSE_MAX_BYTES=131072
PLAINWIRE_APP_INTERACTION_CONCURRENCY=8
PLAINWIRE_APP_INTERACTION_TIMEOUT_MS=10000
```

Keep the loopback exception false in production.

## AI handlers

AI connector keys and optional system prompts are encrypted at rest. Hosted AI execution sends the invoked command and submitted arguments, not arbitrary channel history. Operators should still treat the configured AI endpoint as a data recipient for text users intentionally submit to AI-backed commands.

```ini
PLAINWIRE_AI_COMMAND_CONCURRENCY=4
PLAINWIRE_AI_COMMAND_TIMEOUT_MS=30000
PLAINWIRE_AI_COMMANDS_PER_APP_PER_MINUTE=60
```

Use a provider account/key with the minimum permissions and spending limits appropriate to the deployment.

## Outbound firewall policy

If you run a restrictive egress firewall, allow only providers and destinations you actually use. Generic server-created webhooks can legitimately target many HTTPS destinations, so a strict network allowlist changes product behavior.

## Secrets

Never return provider/application secrets to the browser. Plainwire's TURN, GitHub, KLIPY, interaction, bot, and AI credentials belong on the server side or in the integration worker that owns them.
