#!/usr/bin/env python3
from pathlib import Path
import os, re, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: compare-upstream-env.py /path/to/Plainwire')

root = Path(sys.argv[1]).resolve()
if not root.is_dir():
    raise SystemExit(f'not a directory: {root}')

repo = Path(__file__).resolve().parents[1]
catalog = repo / 'docs/reference/environment-source-catalog.md'
if not catalog.is_file():
    raise SystemExit(f'missing handbook catalog: {catalog}')

pat = re.compile(r'PLAINWIRE_[A-Z0-9_]+')
skip_dirs = {'.git', '_build', 'node_modules', 'site'}


def source_tokens(tree: Path) -> set[str]:
    seen: set[str] = set()
    for dp, dirs, files in os.walk(tree):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fn in files:
            p = Path(dp) / fn
            try:
                text = p.read_text(errors='strict')
            except (OSError, UnicodeDecodeError):
                continue
            seen.update(pat.findall(text))
    return seen


seen = source_tokens(root)
snapshot = set(pat.findall(catalog.read_text()))
added = sorted(seen - snapshot)
removed = sorted(snapshot - seen)

print('Added upstream:')
print('\n'.join('  ' + x for x in added) or '  none')
print('Removed upstream:')
print('\n'.join('  ' + x for x in removed) or '  none')
print(f'Current source tokens: {len(seen)}; handbook catalog: {len(snapshot)}')
