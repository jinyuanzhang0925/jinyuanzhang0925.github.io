"""Validate a built website: routes, assets, original URLs, feeds and search."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.ids = set()
        self.h1s = 0
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError('Duplicate element ID: ' + attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1s += 1
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])


pages = {path: Page(path) for path in DIST.rglob('*.html')}
errors = []
for path, document in pages.items():
    route = '/' + path.relative_to(DIST).as_posix()
    for href in document.links:
        parts = urlsplit(href)
        if parts.scheme or parts.netloc:
            continue
        full = urlsplit(urljoin(route, href))
        target = DIST / unquote(full.path).lstrip('/')
        if target.is_dir():
            target = target / 'index.html'
        if not target.is_file():
            errors.append(f'{route} → missing {href}')
        elif full.fragment and target in pages and unquote(full.fragment) not in pages[target].ids:
            errors.append(f'{route} → missing anchor {href}')

manifest = json.loads((ROOT / 'migration-manifest.json').read_text())
search = json.loads((DIST / 'search.json').read_text())
assert len(search) >= manifest['published_posts']
assert len({p['url'] for p in search}) == len(search)
for post in manifest['posts']:
    assert (DIST / post['url'].lstrip('/') / 'index.html').exists(), post['url']
    assert (ROOT / post['file']).exists(), post['file']
feed = ET.parse(DIST / 'atom.xml')
assert len(feed.findall('{http://www.w3.org/2005/Atom}entry')) == len(search)
ET.parse(DIST / 'sitemap.xml')
assert not any('{{' in p.read_text() for p in pages), 'Unexpanded template'
if errors:
    print('\n'.join(errors))
    raise SystemExit(f'{len(errors)} broken links')
print(f'PASS: {len(pages)} HTML pages, all internal links and anchors, {manifest["published_posts"]} original article URLs, search index, RSS and sitemap.')
