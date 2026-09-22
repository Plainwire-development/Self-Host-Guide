#!/usr/bin/env python3
from pathlib import Path
import html, json, os, re, shutil, sys
try:
    from markdown_it import MarkdownIt
except ImportError:
    raise SystemExit('markdown-it-py is required. Install: python3 -m pip install -r requirements-docs.txt')

ROOT=Path(__file__).resolve().parents[1]
UPSTREAM_VERSION=(ROOT/'UPSTREAM_VERSION').read_text().strip()
UPSTREAM_SERIES='.'.join(UPSTREAM_VERSION.split('.')[:2])
VERIFIED_DATE='2026-09-22'
OUT=Path(os.environ['HANDBOOK_SITE_OUT']) if os.environ.get('HANDBOOK_SITE_OUT') else ROOT/'site'; AS=ROOT/'site-src'/'assets'
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(AS,OUT/'assets')
shutil.copytree(ROOT/'examples',OUT/'examples')
nav=json.loads((ROOT/'site-src/nav.json').read_text())
md=MarkdownIt('commonmark', {'html':False,'linkify':False,'typographer':False}).enable('table')

def slug(s):
    x=re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
    return x or 'section'

def parse_page(path):
    text=path.read_text()
    title=re.search(r'^#\s+(.+)$',text,re.M).group(1).strip()
    hs=[]; seen={}
    for level,name in re.findall(r'^(##|###)\s+(.+)$',text,re.M):
        clean=re.sub(r'[`*_]','',name).strip(); base=slug(clean); n=seen.get(base,0); seen[base]=n+1
        ident=base if n==0 else f'{base}-{n+1}'
        hs.append((len(level),clean,ident))
    html_body=md.render(text)
    # Convert markdown doc links to generated html links.
    html_body=re.sub(r'href="([^"#?]+)\.md(#[^"]*)?"',lambda m:f'href="{m.group(1)}.html{m.group(2) or ""}"',html_body)
    # Add stable ids to h2/h3 in rendered source order. Preserve inline code/markup.
    heading_iter=iter(hs)
    def add_heading_id(m):
        try:
            lvl,name,ident=next(heading_iter)
        except StopIteration:
            return m.group(0)
        return f'<h{lvl} id="{ident}">{m.group(2)}<a class="anchor" href="#{ident}">#</a></h{lvl}>'
    html_body=re.sub(r'<h([23])>(.*?)</h\1>',add_heading_id,html_body,flags=re.S)
    plain=re.sub(r'```.*?```',' ',text,flags=re.S)
    plain=re.sub(r'[#*`>|\[\]()_-]+',' ',plain)
    plain=' '.join(plain.split())
    return title,html_body,hs,plain

def route_for(mdrel): return mdrel[:-3]+'.html'
def depth_root(route):
    depth=len(Path(route).parts)-1
    return '../'*depth

def nav_html(current,rootp):
    out=[]
    for group,items in nav:
        out.append(f'<div class="nav-group"><div class="nav-title">{html.escape(group)}</div>')
        for label,rel in items:
            route=route_for(rel); active=' active' if route==current else ''
            out.append(f'<a class="nav-link{active}" href="{rootp}{route}">{html.escape(label)}</a>')
        out.append('</div>')
    return ''.join(out)

def toc_html(hs):
    if not hs:return ''
    links=''.join(f'<a class="d{lvl}" href="#{ident}">{html.escape(name)}</a>' for lvl,name,ident in hs)
    return f'<details open><summary>On this page</summary>{links}</details>'

def shell(title,body,current,hs,rootp,home=False):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Plainwire {UPSTREAM_SERIES} self-hosting documentation"><meta name="referrer" content="strict-origin-when-cross-origin"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'"><title>{html.escape(title)} | Plainwire Self-Hosting</title><link rel="icon" href="{rootp}assets/logo.svg"><link rel="stylesheet" href="{rootp}assets/style.css"></head><body data-root="{rootp}"><header class="topbar"><div class="top-inner"><a class="skip" href="#content">Skip to content</a><button class="iconbtn menubtn" data-menu aria-label="Open documentation navigation">☰</button><a class="brand" href="{rootp}index.html"><img src="{rootp}assets/logo.svg" alt=""><span>Plainwire Self-Hosting</span></a><span class="version">{UPSTREAM_SERIES}</span><div class="top-actions"><button class="searchbtn" data-search>Search docs <span class="shortcut">Ctrl K</span></button><button class="iconbtn" data-theme-toggle aria-label="Toggle theme">◐</button></div></div></header><div class="layout"><aside class="rail" data-rail>{nav_html(current,rootp)}</aside><div class="rail-scrim" data-rail-scrim></div><main class="main"><article class="content" id="content">{body}<footer class="footer">Plainwire Self-Hosting Handbook · verified against Plainwire {UPSTREAM_VERSION} · {VERIFIED_DATE}</footer></article></main><aside class="toc">{toc_html(hs)}</aside></div><div class="search-modal"><div class="search-box" role="dialog" aria-modal="true" aria-label="Documentation search"><input class="search-input" placeholder="Search configuration, TURN, Redis, Scylla, backups..." aria-label="Search documentation"><div class="results"></div></div></div><script src="{rootp}assets/search-index.js"></script><script src="{rootp}assets/app.js"></script></body></html>'''

search=[]
for group,items in nav:
    for label,rel in items:
        p=ROOT/rel; title,body,hs,plain=parse_page(p); route=route_for(rel); rootp=depth_root(route)
        dest=OUT/route; dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(shell(title,body,route,hs,rootp),encoding='utf-8')
        search.append({'title':title,'path':route,'summary':plain[:180]+'...' if len(plain)>180 else plain,'text':plain})

home=f'''<section class="hero"><div class="eyebrow">Plainwire {UPSTREAM_SERIES} operator handbook</div><h1>Run Plainwire on infrastructure you understand.</h1><p class="lede">Install, configure, administer, and upgrade a Plainwire 2.5 host. PostgreSQL is required. Redis and ScyllaDB stay off until you turn them on.</p><div class="hero-actions"><a class="btn primary" href="docs/getting-started/quickstart.html">Deploy Plainwire</a><a class="btn" href="docs/operations/upgrade-2.2-to-2.5.html">Upgrade to 2.5</a><a class="btn" href="docs/reference/production-checklist.html">Launch checklist</a></div></section><section><div class="stack"><div class="node"><b>PostgreSQL</b><span>Required. Accounts, permissions, and the default message store</span></div><div class="node"><b>Redis</b><span>Optional. Presence, rate gates, and a hot cache</span></div><div class="node"><b>ScyllaDB</b><span>Optional. High-volume history after an explicit migration</span></div></div><div class="callout"><b>Smallest public layout</b>Plainwire, PostgreSQL, an HTTPS reverse proxy, and TURN for calls across networks. Add Redis when you want shared presence and distributed rate gates. Leave messages on PostgreSQL until Scylla has been migrated and verified.</div><div class="grid"><a class="card" href="docs/getting-started/quickstart.html"><h3>Install a host</h3><p>DNS, Docker or a native release, PostgreSQL, HTTPS, and a first health check.</p></a><a class="card" href="docs/configuration/admin-control-plane.html"><h3>Administer accounts</h3><p>Bootstrap the first owner, then disable, restore, or sign out an account.</p></a><a class="card" href="docs/configuration/mail.html"><h3>Turn mail on</h3><p>Self-hosted password reset and verification stay off until SMTP is configured.</p></a><a class="card" href="docs/realtime/webrtc.html"><h3>Make calls reliable</h3><p>TURN, seat registration, roster snapshots, and what the outgoing call UI shows.</p></a><a class="card" href="docs/operations/upgrades.html"><h3>Upgrade safely</h3><p>Back up first. Existing installs apply database migration 53 on startup.</p></a><a class="card" href="docs/operations/backups.html"><h3>Plan recovery</h3><p>Back up PostgreSQL, uploads, encryption keys, and the admin instance secret.</p></a></div></section>'''
(OUT/'index.html').write_text(shell('Home',home,'',[],''),encoding='utf-8')
(OUT/'search-index.json').write_text(json.dumps(search,separators=(',',':')),encoding='utf-8')
(OUT/'assets'/'search-index.js').write_text('window.PLAINWIRE_DOC_INDEX='+json.dumps(search,separators=(',',':')).replace('<','\\u003c')+';',encoding='utf-8')
(OUT/'.nojekyll').write_text('',encoding='utf-8')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
(OUT/'404.html').write_text(shell('Not found','<section class="hero"><div class="eyebrow">404</div><h1>Page not found.</h1><p class="lede">The documentation moved or the address is wrong.</p><div class="hero-actions"><a class="btn primary" href="index.html">Documentation home</a></div></section>','',[],''),encoding='utf-8')
print(f'Built {len(search)} documentation pages into {OUT}')
