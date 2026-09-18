#!/usr/bin/env python3
from pathlib import Path
import argparse, re

CATEGORY_ORDER = [
    'Core and public runtime', 'Database', 'Uploads and media', 'HTTP and WebSocket',
    'Realtime and TURN', 'Admin control plane', 'Redis', 'Scylla and message storage',
    'Webhooks and integrations', 'Build, development, and internal'
]

def category(v):
    if v.startswith('PLAINWIRE_DB_') or v == 'PLAINWIRE_ALLOW_INSECURE_DB' or v == 'PLAINWIRE_POSTGRES_SERVICE': return 'Database'
    if v.startswith('PLAINWIRE_UPLOAD_') or v.startswith('PLAINWIRE_MEDIA_') or v.startswith('PLAINWIRE_FILE_') or v in {'PLAINWIRE_PROFILE_IMAGE_MAX_BYTES','PLAINWIRE_COMPRESS_OVERSIZE_UPLOADS','PLAINWIRE_ALLOW_ARBITRARY_MEDIA','PLAINWIRE_ALLOW_UNSIGNED_MEDIA_TOKENS'}: return 'Uploads and media'
    if v.startswith('PLAINWIRE_HTTP_') or v.startswith('PLAINWIRE_WS_') or v in {'PLAINWIRE_ALLOWED_ORIGINS','PLAINWIRE_TRUSTED_PROXIES','PLAINWIRE_TRUST_PROXY'}: return 'HTTP and WebSocket'
    if v.startswith('PLAINWIRE_TURN_') or v.startswith('PLAINWIRE_CF_') or v.startswith('PLAINWIRE_STUN_') or v.startswith('PLAINWIRE_RTC_') or v.startswith('PLAINWIRE_VOICE_') or v in {'PLAINWIRE_REQUIRE_TURN','PLAINWIRE_ICE_TRANSPORT_POLICY','PLAINWIRE_CALL_RING_MS'}: return 'Realtime and TURN'
    if v.startswith('PLAINWIRE_ADMIN_'): return 'Admin control plane'
    if v.startswith('PLAINWIRE_REDIS_') or v == 'PLAINWIRE_NODE_ID': return 'Redis'
    if v.startswith('PLAINWIRE_SCYLLA_') or v.startswith('PLAINWIRE_STORAGE_') or v in {'PLAINWIRE_MESSAGE_BACKEND','PLAINWIRE_MESSAGE_NODE_ID','PLAINWIRE_MESSAGE_ID_CLOCK_ROLLBACK_MS','PLAINWIRE_INSTANCE_ID'}: return 'Scylla and message storage'
    if v.startswith('PLAINWIRE_WEBHOOK_') or v.startswith('PLAINWIRE_GITHUB_') or v.startswith('PLAINWIRE_KLIPY_') or v == 'PLAINWIRE_BOT_TOKEN': return 'Webhooks and integrations'
    if v.startswith('PLAINWIRE_TEST_') or v.startswith('PLAINWIRE_DEV_') or v.startswith('PLAINWIRE_BUILD_') or v in {'PLAINWIRE_APP_USER','PLAINWIRE_ASSET_VERSION','PLAINWIRE_CLIENT_CONFIG','PLAINWIRE_DEBUG','PLAINWIRE_HOST','PLAINWIRE_RELEASE_BIN','PLAINWIRE_RTC_CONFIG','PLAINWIRE_VERSION__'}: return 'Build, development, and internal'
    return 'Core and public runtime'

MANUAL = {
'PLAINWIRE_ADMIN_BOOTSTRAP_TOKEN':'Sensitive bootstrap token name recognized by storage/config sanitization. Treat as secret. Prefer the documented enrollment/recovery flow rather than inventing a permanent admin key.',
'PLAINWIRE_ADMIN_IDLE_TIMEOUT_MS':'Admin HTTP listener idle timeout. Default 30000 ms, clamped to 5000 through 120000.',
'PLAINWIRE_ADMIN_MAX_KEEPALIVE':'Maximum admin listener keepalive count. Default 200, clamped to 1 through 2000.',
'PLAINWIRE_ADMIN_REQUEST_TIMEOUT_MS':'Admin listener request timeout. Default 15000 ms, clamped to 5000 through 60000.',
'PLAINWIRE_ALLOWED_ORIGINS':'Comma-separated WebSocket origin allowlist. If unset, Plainwire derives the normal production origin from the public URL. Set explicitly for unusual multi-origin deployments.',
'PLAINWIRE_ALLOW_ARBITRARY_MEDIA':'Compatibility override allowing remote media outside the normal production restrictions. Default false. Avoid in production unless the egress risk is understood.',
'PLAINWIRE_ALLOW_INSECURE_DB':'Explicit production exception for PostgreSQL without TLS. Use only when the DB path is fully trusted, such as a private same-host/container network.',
'PLAINWIRE_ALLOW_STATIC_TURN_CREDENTIALS':'Allows static TURN username/password credentials in production. Default false. Prefer short-lived coturn shared-secret or Cloudflare credentials.',
'PLAINWIRE_ALLOW_UNSIGNED_MEDIA_TOKENS':'Compatibility override for unsigned media tokens in production. Default false. Do not enable as a routine deployment setting.',
'PLAINWIRE_APP_USER':'OpenRC install/update helper override for the Unix account that owns the Plainwire checkout. Not an application runtime setting.',
'PLAINWIRE_ASSET_VERSION':'Optional runtime asset fingerprint override. Normally let Plainwire derive its asset version from the build.',
'PLAINWIRE_BOT_TOKEN':'Example environment variable used by the Erlang bot SDK documentation. It is not a core Plainwire server setting.',
'PLAINWIRE_BUILD_MEDIA_QUALITY':'Release helper switch controlling whether the optional native media-quality worker is built. Defaults to 0 in packaging scripts.',
'PLAINWIRE_BUILD_PROFILE':'Release helper rebar profile override. Packaging scripts default it to `default`.',
'PLAINWIRE_CALL_RING_MS':'Call ring timeout. Defaults to the server ring constant and is clamped between 10000 and 120000 ms.',
'PLAINWIRE_CLIENT_CONFIG':'Browser global populated by bootstrap code. This is not a server environment variable to set in `.env`.',
'PLAINWIRE_DEBUG':'Browser/test debug flag. Not a normal server environment variable.',
'PLAINWIRE_DEV_DB_DIR':'Development PostgreSQL helper data directory. Defaults below XDG data home or `~/.local/share/plainwire/postgres`.',
'PLAINWIRE_DEV_DB_LOG':'Development database helper log path. Defaults to `postgres.log` under the helper socket directory.',
'PLAINWIRE_DEV_DB_SOCKET_DIR':'Development database helper socket directory. Defaults to the parent of the development DB data directory.',
'PLAINWIRE_HOST':'Hostname variable consumed by the upstream Caddy example. It is a proxy-template variable, not the Plainwire public URL setting.',
'PLAINWIRE_ICE_TRANSPORT_POLICY':'WebRTC ICE policy. `all` is normal. `relay` forces TURN and is useful for controlled relay tests.',
'PLAINWIRE_MEDIA_QUALITY_BIN':'Absolute path override for the optional native media-quality executable.',
'PLAINWIRE_MEDIA_SIGNING_KEY':'Optional dedicated media-token signing key. Keep secret. Source install helpers generate/configure it when needed.',
'PLAINWIRE_POSTGRES_SERVICE':'OpenRC installer override naming the PostgreSQL service to manage/discover. Not used by normal app runtime.',
'PLAINWIRE_RELEASE_BIN':'Path to an installed relx `plainwire_relay` executable used by migration/benchmark helper scripts for RPC.',
'PLAINWIRE_RTC_CONFIG':'Browser global holding fetched ICE configuration. Not a server environment variable.',
'PLAINWIRE_SCYLLA_CACHE_TTL_MS':'Scylla-side message cache TTL. Default 20000 ms, clamped to 1000 through 300000.',
'PLAINWIRE_SCYLLA_MAX_PAGE_SCAN_ROWS':'Upper bound for rows scanned while serving a paged Scylla history request. Default 4096 in the Scylla message store.',
'PLAINWIRE_SCYLLA_MIGRATION_MODE':'Migration behavior selector. Source default is `manual`. Use the documented storage migration commands rather than changing this casually.',
'PLAINWIRE_SCYLLA_PARITY_SAMPLE_ROWS':'Rows sampled by parity checks. Default 500, clamped to 50 through 5000.',
'PLAINWIRE_SCYLLA_REPLICATION_FACTOR':'Replication factor used by the explicit Scylla migration script when creating schema. Script default is 1 and is only suitable for a single-node/lab topology.',
'PLAINWIRE_SCYLLA_VERIFY_AFTER_ID':'Starting message ID for storage verification. Default 0.',
'PLAINWIRE_SCYLLA_VERIFY_LIMIT':'Maximum rows for a verification batch. Default 1000, clamped to 1 through 5000.',
'PLAINWIRE_STUN_URLS':'Comma-separated STUN URL override. Source default includes Google public STUN at `stun:stun.l.google.com:19302`.',
'PLAINWIRE_TEST_BOOL':'Internal EUnit fixture for environment parsing tests. Do not configure in production.',
'PLAINWIRE_TEST_CQLSH_LOG':'Browser/tool test fixture used to capture fake `cqlsh` invocations. Do not configure in production.',
'PLAINWIRE_TEST_NATIVE':'Test switch enabling native media-quality integration tests. Do not configure in production.',
'PLAINWIRE_TRUSTED_PROXIES':'Trusted reverse-proxy CIDRs. Default source value is `127.0.0.1/32,::1/128`. Keep narrow.',
'PLAINWIRE_TURN_CREDENTIAL':'Static TURN credential compatibility setting. Production requires the explicit static-credential override. Prefer short-lived credentials.',
'PLAINWIRE_VERSION__':'Build-time HTML placeholder token, not an environment variable.',
'PLAINWIRE_VOICE_MAX_PARTICIPANTS':'Voice room participant cap. Default 8, clamped to 2 through 32.',
'PLAINWIRE_VOICE_MAX_SHARES':'Concurrent screen-share cap. Default 2, clamped to 1 through 8.',
'PLAINWIRE_WEBHOOK_ALLOW_HTTP':'Allows plain HTTP webhook targets. Default false. Keep false for normal production internet egress.',
'PLAINWIRE_WEBHOOK_CONCURRENCY':'Webhook dispatcher concurrency. Default 8, clamped to 1 through 32.'
}

DANGEROUS = {
    'PLAINWIRE_ALLOW_ARBITRARY_MEDIA','PLAINWIRE_ALLOW_INSECURE_DB','PLAINWIRE_ALLOW_STATIC_TURN_CREDENTIALS',
    'PLAINWIRE_ALLOW_UNSIGNED_MEDIA_TOKENS','PLAINWIRE_REDIS_TLS_INSECURE','PLAINWIRE_WEBHOOK_ALLOW_HTTP'
}
SECRET_PARTS = ('PASS','PASSWORD','SECRET','TOKEN','KEY_ID','API_TOKEN','ENC_KEY','CREDENTIAL','SIGNING_KEY')

def all_text_files(root):
    skip={'.git','node_modules','_build','site'}
    for p in root.rglob('*'):
        if not p.is_file() or any(x in skip for x in p.parts): continue
        try: p.read_text()
        except UnicodeDecodeError: continue
        yield p

def source_vars(root):
    found={}
    rx=re.compile(r'PLAINWIRE_[A-Z0-9_]+')
    for p in all_text_files(root):
        rel=p.relative_to(root).as_posix()
        for n,line in enumerate(p.read_text(errors='ignore').splitlines(),1):
            for v in rx.findall(line):
                found.setdefault(v,[]).append((rel,n,line.strip()))
    return found

def parse_env(root):
    p=root/'.env.example'
    data={}
    comments=[]
    for raw in p.read_text().splitlines():
        line=raw.strip()
        if not line:
            comments=[]; continue
        if line.startswith('#'):
            comments.append(line.lstrip('#').strip()); continue
        m=re.match(r'([A-Z][A-Z0-9_]+)=(.*)$',raw)
        if m:
            v,val=m.groups()
            data[v]={'value':val.strip(),'comment':' '.join(comments).strip()}
            comments=[]
    return data

def code_default(hits):
    pats=[
      re.compile(r'env_(?:int|bool|str|range)\("[A-Z0-9_]+",\s*(<<"[^"]*">>|"[^"]*"|[0-9]+|true|false)'),
      re.compile(r'os:getenv\("[A-Z0-9_]+",\s*"([^"]*)"\)'),
    ]
    for _,_,line in hits:
        for pat in pats:
            m=pat.search(line)
            if m: return m.group(1)
    return ''

def clean_comment(v, comment):
    if v in MANUAL: return MANUAL[v]
    if comment:
        c=comment[0].upper()+comment[1:] if comment else comment
        return c
    # useful fallback by component
    comp=category(v)
    return f'Advanced {comp.lower()} setting present in the Plainwire 2.0 source. Keep the source default unless the subsystem guide or a measured production need calls for an override.'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('upstream',type=Path)
    ap.add_argument('--output',type=Path,default=Path('docs/reference/environment-source-catalog.md'))
    args=ap.parse_args()
    root=args.upstream.resolve(); env=parse_env(root); found=source_vars(root)
    vars_=sorted(found)
    lines=['# Complete environment and source token catalog','',
      'This appendix is generated from the Plainwire 2.0 source tree. It lists every `PLAINWIRE_*` token found in the snapshot, including normal operator settings, build helpers, browser globals, and test-only names.', '',
      '> Do not copy this table into `.env`. Most installations should use the upstream `.env.example` plus the subsystem guides. This catalog exists so obscure knobs are not invisible.', '',
      f'Catalog size: **{len(vars_)} tokens**. Upstream `.env.example` contains **{len(env)} configured names**.', '']
    for cat in CATEGORY_ORDER:
        group=[v for v in vars_ if category(v)==cat]
        if not group: continue
        lines += [f'## {cat}','', '| Name | Example/default | Purpose | Source |', '| --- | --- | --- | --- |']
        for v in group:
            e=env.get(v,{})
            val=e.get('value','')
            if not val:
                val=code_default(found[v])
            if any(x in v for x in SECRET_PARTS):
                shown='secret / unset' if not val or 'replace' in val.lower() else ('empty by default' if val=='' else val)
            else:
                shown=val or 'source-managed / unset'
            desc=clean_comment(v,e.get('comment',''))
            if v in DANGEROUS: desc='**Compatibility/security exception.** '+desc
            loc=[]
            for rel,n,_ in found[v]:
                item=f'`{rel}:{n}`'
                if item not in loc: loc.append(item)
                if len(loc)>=3: break
            lines.append(f'| `{v}` | {shown.replace("|","\\|")} | {desc.replace("|","\\|")} | {"<br>".join(loc)} |')
        lines.append('')
    lines += ['## Regenerate after an upstream upgrade','', '```sh', 'python3 scripts/rebuild-env-reference.py /path/to/Plainwire', 'python3 scripts/build-site.py', '```','',
      'Review the diff. A new variable is not automatically a setting operators should change. Document its operational meaning before using it in production.', '']
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text('\n'.join(lines))
    print(f'wrote {args.output} with {len(vars_)} tokens')

if __name__=='__main__': main()
