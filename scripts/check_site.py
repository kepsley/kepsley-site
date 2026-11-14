#!/usr/bin/env python3
"""Validate the public deployment tree without contacting external services."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1] / 'site'
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.lang = None; self.viewport = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'meta' and a.get('name') == 'viewport': self.viewport = True
        for key in ('href', 'src'):
            if key in a: self.links.append(a[key])

pages = sorted(ROOT.rglob('*.html'))
assert len(pages) == 9, f'Expected nine pages, got {len(pages)}'
for page in pages:
    html = page.read_text(); doc = Links(); doc.feed(html)
    assert doc.lang in ('en', 'zh-Hans', 'ja'), page
    assert doc.viewport and 'Kepsley' in html and 'iCloud' in html, page
    assert 'linsora.icqnft.com' not in html and 'privacy.kepsley.com' not in html, page
    for link in doc.links:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc or not parts.path: continue
        target = ((ROOT / parts.path.lstrip('/')) if parts.path.startswith('/') else (page.parent / unquote(parts.path))).resolve()
        assert target.is_relative_to(ROOT), (page, link)
        if target.is_dir(): target /= 'index.html'
        assert target.is_file(), (page, link)
for file in ROOT.rglob('*'):
    if file.is_file(): assert file.suffix in ('.html', '.css') or file.name == '.nojekyll', file
print('PASS: nine localized pages, local links, viewport and public-file allowlist')
