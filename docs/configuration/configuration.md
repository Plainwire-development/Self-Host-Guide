# Production configuration

Plainwire reads production configuration from environment variables. Treat the environment file as a secret-bearing configuration artifact.

## Required production identity

```ini
PLAINWIRE_ENV=production
PLAINWIRE_PUBLIC_URL=https://chat.example.com
COOKIE_SECURE=true
PLAINWIRE_TRUST_PROXY=true
```

## Database

Set a dedicated PostgreSQL database and role. For remote databases, enable TLS.

```ini
PLAINWIRE_DB_HOST=db.internal
PLAINWIRE_DB_PORT=5432
PLAINWIRE_DB_USER=plainwire
PLAINWIRE_DB_PASS=CHANGE_ME
PLAINWIRE_DB_NAME=plainwire
PLAINWIRE_DB_SSL=true
```

Production startup intentionally checks important security settings. Do not bypass TLS or cookie checks simply to make a deployment start.

## Encryption key

Generate a 32-byte key and store its base64 form:

```sh
openssl rand -base64 32
```

```ini
PLAINWIRE_ENC_KEY=CHANGE_ME
```

Back this key up securely. Replacing it can make previously encrypted data unreadable.

## Realtime storage

Recommended 2.0 baseline:

```ini
PLAINWIRE_REDIS_ENABLED=true
PLAINWIRE_MESSAGE_BACKEND=postgres
PLAINWIRE_SCYLLA_ENABLED=false
```

Redis can be enabled early. Scylla should be introduced through the documented migration.

## Calls

Public call deployments should configure TURN and normally set:

```ini
PLAINWIRE_REQUIRE_TURN=true
```

## Registration

```ini
PLAINWIRE_REGISTRATION_ENABLED=true
```

Disable registration for invite-only or closed instances.

## Advanced reference

The complete operator variable list is in [Environment variable reference](../reference/environment.md). Do not copy every optional variable into production. Explicitly configure what you operate and keep the rest on well-understood defaults.
