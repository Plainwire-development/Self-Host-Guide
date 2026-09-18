#!/usr/bin/env python3
from pathlib import Path
import base64, os, re, sys

if len(sys.argv) != 2:
    raise SystemExit("usage: verify-production-env.py /path/to/plainwire.env")
path = Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(f"not found: {path}")

env = {}
for raw in path.read_text(errors="replace").splitlines():
    line = raw.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k,v=line.split('=',1)
    env[k.strip()] = v.strip().strip('"').strip("'")

problems=[]; warnings=[]
def need(k):
    if not env.get(k): problems.append(f"missing {k}")

def truth(k): return env.get(k,'').lower() in {'1','true','yes','on'}

if env.get('PLAINWIRE_ENV') not in {'prod','production'}: problems.append('PLAINWIRE_ENV is not production')
need('PLAINWIRE_PUBLIC_URL')
if env.get('PLAINWIRE_PUBLIC_URL','').startswith('http://'): problems.append('PLAINWIRE_PUBLIC_URL uses http://')
if not truth('COOKIE_SECURE'): problems.append('COOKIE_SECURE is not true')
for k in ['PLAINWIRE_DB_HOST','PLAINWIRE_DB_USER','PLAINWIRE_DB_PASS','PLAINWIRE_DB_NAME','PLAINWIRE_ENC_KEY']:
    need(k)
for k,v in env.items():
    if 'CHANGE_ME' in v or v.lower() in {'password','plainwire','changeme','replace-me'}:
        if k.endswith(('PASS','PASSWORD','SECRET','KEY','TOKEN','CREDENTIAL')) or k in {'PLAINWIRE_DB_PASS'}:
            problems.append(f'{k} still looks like a placeholder')
enc=env.get('PLAINWIRE_ENC_KEY','')
if enc:
    try:
        if len(base64.b64decode(enc, validate=True)) != 32: problems.append('PLAINWIRE_ENC_KEY is not a base64-encoded 32-byte value')
    except Exception: problems.append('PLAINWIRE_ENC_KEY is not valid base64')
if truth('PLAINWIRE_REDIS_ENABLED') and not env.get('PLAINWIRE_REDIS_PASSWORD'):
    warnings.append('Redis is enabled without PLAINWIRE_REDIS_PASSWORD. This may be intentional only on a tightly isolated deployment.')
if env.get('PLAINWIRE_DB_SSL','').lower() in {'0','false','no','off'} and not truth('PLAINWIRE_ALLOW_INSECURE_DB'):
    problems.append('database TLS is disabled without the explicit PLAINWIRE_ALLOW_INSECURE_DB exception')
if truth('PLAINWIRE_REQUIRE_TURN'):
    cf_ok = bool(env.get('PLAINWIRE_CF_TURN_KEY_ID') and env.get('PLAINWIRE_CF_TURN_API_TOKEN'))
    coturn_ok = bool(env.get('PLAINWIRE_TURN_URLS') and env.get('PLAINWIRE_TURN_SECRET'))
    static_ok = bool(truth('PLAINWIRE_ALLOW_STATIC_TURN_CREDENTIALS') and env.get('PLAINWIRE_TURN_URLS') and env.get('PLAINWIRE_TURN_USERNAME') and env.get('PLAINWIRE_TURN_CREDENTIAL'))
    if not (cf_ok or coturn_ok or static_ok): problems.append('PLAINWIRE_REQUIRE_TURN is true but no complete Cloudflare, shared-secret, or explicitly allowed static TURN configuration was found')
backend=env.get('PLAINWIRE_MESSAGE_BACKEND','postgres')
if backend not in {'postgres','dual','scylla'}: problems.append('PLAINWIRE_MESSAGE_BACKEND must be postgres, dual, or scylla')
if backend in {'dual','scylla'} and not truth('PLAINWIRE_SCYLLA_ENABLED'):
    warnings.append('Scylla backend mode implicitly requires Scylla. Set PLAINWIRE_SCYLLA_ENABLED=true for clarity.')
if truth('PLAINWIRE_ADMIN_ALLOW_REMOTE') and not env.get('PLAINWIRE_ADMIN_PUBLIC_URL','').startswith('https://'):
    problems.append('remote admin access requires an HTTPS PLAINWIRE_ADMIN_PUBLIC_URL')
if env.get('PLAINWIRE_ICE_TRANSPORT_POLICY') == 'relay':
    warnings.append('ICE policy is relay-only. This increases TURN usage and is often meant for diagnostics.')
if env.get('PLAINWIRE_ALLOW_STATIC_TURN_CREDENTIALS','').lower() in {'1','true','yes','on'}:
    warnings.append('static TURN credentials are explicitly allowed in production')
if truth('PLAINWIRE_REDIS_TLS_INSECURE'):
    problems.append('PLAINWIRE_REDIS_TLS_INSECURE is enabled')

print(f"Checked {path}")
for p in problems: print(f"ERROR: {p}")
for p in warnings: print(f"WARN:  {p}")
if not problems and not warnings: print('OK: no obvious production configuration problems found')
elif not problems: print('OK with warnings')
raise SystemExit(1 if problems else 0)
