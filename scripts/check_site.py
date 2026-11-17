#!/usr/bin/env python3
"""Validate public pages, metadata, anchors and deployable assets without a network."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'site'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.anchors=[]; self.lang=None; self.meta={}; self.rels=[]; self.ids=set(); self.h1=0; self.scripts=0; self.images=[]; self.events=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a':self.anchors.append(a)
        if tag=='html':self.lang=a.get('lang')
        if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link':self.rels.append(a)
        if tag=='h1':self.h1+=1
        if tag=='script':self.scripts+=1
        if tag=='img':self.images.append(a)
        if 'id' in a:
            assert a['id'] not in self.ids, ('duplicate id',a['id'])
            self.ids.add(a['id'])
        self.events += [key for key in a if key.startswith('on')]
        for key in ('href','src'):
            if key in a:self.links.append(a[key])

def parse(path):
    doc=Page();doc.feed(path.read_text());return doc

pages=sorted(ROOT.rglob('*.html'))
assert len(pages)==9, f'Expected nine pages, got {len(pages)}'
home_paths={ROOT/'index.html':('en',''),ROOT/'zh/index.html':('zh-Hans','zh/'),ROOT/'ja/index.html':('ja','ja/')}
parsed={path:parse(path) for path in pages}
for page,doc in parsed.items():
    html=page.read_text()
    assert doc.lang in ('en','zh-Hans','ja'),page
    assert doc.meta.get('viewport') and 'Kepsley' in html and doc.h1==1,page
    assert not doc.scripts and not doc.events, ('Unexpected scripts/events',page)
    assert 'linsora.icqnft.com' not in html and 'privacy.kepsley.com' not in html,page
    if page in home_paths:
        lang,route=home_paths[page];url='https://www.kepsley.com/'+route
        assert doc.lang==lang and doc.meta.get('description'),page
        assert doc.meta.get('og:url')==url and doc.meta.get('og:title') and doc.meta.get('og:description'),page
        assert doc.meta.get('og:image')=='https://www.kepsley.com/assets/share.png',page
        assert doc.meta.get('twitter:card')=='summary_large_image',page
        assert any(a.get('rel')=='canonical' and a.get('href')==url for a in doc.rels),page
        assert {a.get('hreflang') for a in doc.rels if a.get('rel')=='alternate'}=={'en','zh-Hans','ja','x-default'},page
        assert {'main','how','moments','about'}.issubset(doc.ids),page
        assert all('alt' in image and 'width' in image and 'height' in image for image in doc.images),page
        assert not any(term in html.lower() for term in ['testflight.apple.com','<form','<iframe']),page
        downloads=[a for a in doc.anchors if 'download-link' in a.get('class','').split()]
        assert len(downloads)==1 and downloads[0].get('href')=='https://apps.apple.com/app/id6817633126',page
        assert downloads[0].get('target','_self')=='_self',page
        assert [link for link in doc.links if urlsplit(link).hostname=='apps.apple.com']==['https://apps.apple.com/app/id6817633126'],page
        assert any(a.get('class')=='primary-link' and a.get('href')=='#how' for a in doc.anchors),page
        assert 'home.css' in html and 'style.css' not in html,page
    else:
        assert 'iCloud' in html and 'documents.css' in html and 'home.css' not in html,page
        assert {'top','main','section-01','heading-01','contact-title'}.issubset(doc.ids),page
        assert doc.meta.get('description') and doc.meta.get('og:url'),page
        assert any(a.get('rel')=='canonical' and a.get('href')==doc.meta['og:url'] for a in doc.rels),page
        assert {a.get('hreflang') for a in doc.rels if a.get('rel')=='alternate'}=={'en','zh-Hans','ja','x-default'},page
        assert 'mailto:otsgame@yahoo.com' in doc.links,page
    for link in doc.links:
        parts=urlsplit(link)
        if parts.scheme or parts.netloc:continue
        target=page if not parts.path else ((ROOT/parts.path.lstrip('/')) if parts.path.startswith('/') else (page.parent/unquote(parts.path))).resolve()
        assert target.is_relative_to(ROOT),(page,link)
        if target.is_dir():target/='index.html'
        assert target.is_file(),(page,link)
        if parts.fragment:
            assert target.suffix=='.html' and unquote(parts.fragment) in parsed[target].ids,(page,link)
allowed={'.html','.css','.svg','.png','.webp'}
for file in ROOT.rglob('*'):
    if not file.is_file():continue
    assert file.suffix in allowed or file.name=='.nojekyll',file
    if file.suffix=='.svg':
        tree=ET.fromstring(file.read_text())
        for element in tree.iter():
            assert element.tag.rsplit('}',1)[-1] not in ('script','foreignObject'),file
            assert not any(k.startswith('on') for k in element.attrib),file
assert (ROOT/'assets/share.png').is_file(),'Missing raster share image'
subprocess.run([sys.executable,str(Path(__file__).with_name('build_home.py')),'--check'],check=True)
subprocess.run([sys.executable,str(Path(__file__).with_name('build_documents.py')),'--check'],check=True)
print('PASS: nine pages; three brand homes; SEO metadata; anchors; local links; static public assets')
