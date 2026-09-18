import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if 'id' in d: self.ids.add(d['id'])
        if tag in {'a','link'} and d.get('href'): self.links.append(d['href'])
        if tag in {'script','img'} and d.get('src'): self.links.append(d['src'])

class SiteLinkTests(unittest.TestCase):
    def test_local_links_resolve(self):
        errors=[]
        for page in SITE.rglob('*.html'):
            parser=LinkParser(); parser.feed(page.read_text())
            for href in parser.links:
                u=urlsplit(href)
                if u.scheme or href.startswith('//') or href.startswith('mailto:'): continue
                if not u.path:
                    if u.fragment and u.fragment not in parser.ids:
                        errors.append(f'{page.relative_to(SITE)} missing anchor #{u.fragment}')
                    continue
                target=(page.parent/u.path).resolve()
                try: target.relative_to(SITE.resolve())
                except ValueError:
                    errors.append(f'{page.relative_to(SITE)} escapes site: {href}'); continue
                if not target.exists(): errors.append(f'{page.relative_to(SITE)} missing {href}')
        self.assertFalse(errors, '\n'.join(errors[:100]))

    def test_no_markdown_links_in_rendered_site(self):
        bad=[]
        for page in SITE.rglob('*.html'):
            if 'href="' in page.read_text():
                for part in page.read_text().split('href="')[1:]:
                    href=part.split('"',1)[0]
                    if href.split('#',1)[0].endswith('.md'): bad.append((page,href))
        self.assertFalse(bad,bad[:20])

if __name__=='__main__': unittest.main()
