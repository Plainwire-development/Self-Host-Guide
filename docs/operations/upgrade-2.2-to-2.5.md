# Plainwire 2.2 to 2.5

Plainwire 2.5.0 is the current handbook target. An existing database applies pending migrations when the database process starts. A 2.2 database picks up migrations 51, 52, and 53 on the way to 2.5.0. Migration 53 is the one 2.5.0 itself adds.

PostgreSQL stays required. Redis and ScyllaDB stay optional. Erlang/OTP 27, 28, and 29 are supported. There is no new required environment variable for a PostgreSQL-only host that does not send mail.

## What each release changes

### 2.3.0

Voice-note playback and recording reliability. No database migration and no Bot API change. Existing 2.2 workers keep working.

### 2.4.0

Developer Applications can connect a hosted model (OpenAI, Anthropic, Gemini, OpenRouter, Groq, Mistral, Ollama, or another OpenAI-compatible endpoint) without a custom worker. Mention chat is opt-in. A loopback destination such as Ollama still needs `PLAINWIRE_APP_ALLOW_LOOPBACK_HTTP=true`.

Migration 51 adds AI provider, chat-trigger, and context columns on `developer_applications`.

The host panel's ban, suspend, and restore buttons submit `POST /api/users/:id/moderation` again.

### 2.4.1

Accounts can store an optional email and verify it. Password reset goes only to a verified address. Migration 52 adds `email` columns on `users` and the `account_tokens` table.

Self-hosted mail stays off unless `PLAINWIRE_MAIL_ENABLED=true` and SMTP is configured. See [Mail](../configuration/mail.md).

### 2.5.0

Migration 53 replaces the check constraint on `instance_account_actions.action` so the log can record `disable`, `revoke_sessions`, `clear_display_name`, `remove_email`, and `resend_verification` in addition to `suspend`, `ban`, and `restore`.

Operators use that same moderation route for the new account actions. There is no second admin API. See [Host admin control plane](../configuration/admin-control-plane.md).

Calls register a voice or call seat before other participants are told someone joined. Roster snapshots (`voice_state` and `call_state`) are not discarded when realtime delivery sheds load. See [WebRTC](../realtime/webrtc.md).

Ordinary channel messages no longer insert an inbox row for every member. See [Notifications](notifications.md).

OTP 29 support depends on `scripts/compile-erlcass.sh`, which the upstream `rebar.config` runs before compiling `erlcass`. A missing native Scylla driver does not fail a PostgreSQL build. See [Build from source](../installation/build-from-source.md).

## Before you upgrade

1. Read this page and the upstream release notes for 2.3.0, 2.4.0, 2.4.1, and 2.5.0.
2. Back up PostgreSQL, uploads, `/etc/plainwire/plainwire.env`, encryption and search keys, and `admin-instance.key` if the control plane is enabled.
3. Keep the running 2.2 (or newer) artifact available.
4. Build on OTP 27, 28, or 29. Confirm `erl -eval 'io:format("~s~n",[erlang:system_info(otp_release)]), halt().' -noshell` prints `27`, `28`, or `29`.
5. Compare configuration:

   ```sh
   python3 scripts/compare-upstream-env.py /path/to/Plainwire
   ```

   Compared with the 2.2 catalog, the 2.5.0 source adds the mail variables and `PLAINWIRE_AI_CHAT_MENTIONS_PER_USER_PER_MINUTE` (default 20). Mail arrived in 2.4.1. Leave `PLAINWIRE_MAIL_ENABLED` unset if you do not want password-reset email.

6. If you run bots, leave them on Bot API v1. 2.3 through 2.5 do not remove those routes.

## Apply the release

Native install: build into a new directory such as `/opt/plainwire/releases/2.5.0`, stop the service, point `/opt/plainwire/current` at it, and start. Container install: start the new image with the same environment file and volumes.

On startup Plainwire takes PostgreSQL advisory lock `578421975` and applies any missing migration inside a transaction. Several nodes starting together still run that sequence one at a time. Watch the service log until `/api/health` succeeds, then check `/api/version` for 2.5.0.

## After startup

- log in, send a channel message, and confirm a non-mentioned member did not gain an inbox row;
- mention someone and confirm that inbox row appears, then open the channel and confirm the row is gone;
- place a call across two networks and confirm the outgoing panel names the people being waited on;
- if the admin plane is enabled, open a non-operator account and confirm disable, restore, and sign-out are present;
- if mail should stay off, confirm `PLAINWIRE_MAIL_ENABLED` is not `true`.

## Rollback

Switch the symlink or image back only after you have confirmed the older build still starts against the migrated database. A symlink change does not undo migrations 51, 52, or 53. If the older build will not start, restore the PostgreSQL backup taken before the upgrade and then start the old release. Do not restore a database backup over a database that newer nodes are still writing.
