#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
nav=json.loads((ROOT/'site-src/nav.json').read_text())
listed={rel for _,items in nav for _,rel in items}
docs={p.relative_to(ROOT).as_posix() for p in (ROOT/'docs').rglob('*.md')}
for missing in sorted(docs-listed): errors.append(f'doc not in site nav: {missing}')
for missing in sorted(listed-docs): errors.append(f'nav target missing: {missing}')
for p in [ROOT/'README.md',*sorted((ROOT/'docs').rglob('*.md'))]:
    text=p.read_text()
    rel=p.relative_to(ROOT)
    if chr(0x2014) in text or chr(0x2013) in text: errors.append(f'{rel}: contains forbidden long dash')
    if not re.search(r'^#\s+\S',text,re.M): errors.append(f'{rel}: missing H1')
    # local markdown links
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        if '://' in target or target.startswith('#') or target.startswith('mailto:'): continue
        target=target.split('#',1)[0]
        if not target: continue
        dest=(p.parent/target).resolve()
        if not dest.exists(): errors.append(f'{rel}: broken link {target}')
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in {'.md','.html','.css','.js','.py','.yaml','.yml','.conf','.example'}:
        try:t=p.read_text()
        except UnicodeDecodeError:continue
        if chr(0x2014) in t or chr(0x2013) in t: errors.append(f'{p.relative_to(ROOT)}: contains forbidden long dash')
if errors:
    print('\n'.join('ERROR: '+e for e in errors)); raise SystemExit(1)
print(f'OK: {len(docs)} docs, navigation complete, local Markdown links resolve, no em/en dashes')
