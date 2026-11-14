#!/usr/bin/env python3
"""Render six static support/privacy pages while keeping their approved body copy intact."""
from pathlib import Path
from html import escape
import argparse
import json
from build_home import CONTENT, icon

ROOT = Path(__file__).resolve().parents[1] / 'site'
SOURCE = json.loads(Path(__file__).with_name('document_content.json').read_text())
LABELS = {
    'en': dict(home='Home', breadcrumb='Page navigation', toc='On this page', back='Back to top', privacy_kicker='Privacy & your choices', support_kicker='Here to help', privacy_intro='How Kepsley handles your recordings, text and service connections. Find the details below, section by section.', support_intro='A little guidance, whenever you need it. Find help with recording, AI tools, backups and more.', help='Need a hand?', email='Contact support', email_note='Email us with your app version and a description of what happened.', docs='Kepsley guide', section='Section'),
    'zh-Hans': dict(home='首页', breadcrumb='页面导航', toc='本页目录', back='回到顶部', privacy_kicker='隐私与选择', support_kicker='随时为你提供帮助', privacy_intro='了解 Kepsley 如何处理录音、文字与服务连接。按章节查看与你有关的具体说明。', support_intro='需要的时候，总有一份清晰的指引。在这里查找录音、AI 工具、备份等功能的使用帮助。', help='需要帮助？', email='联系支持', email_note='请在邮件中附上 App 版本，并描述遇到的问题。', docs='Kepsley 使用指南', section='章节'),
    'ja': dict(home='ホーム', breadcrumb='ページナビゲーション', toc='このページの目次', back='ページの先頭へ', privacy_kicker='プライバシーと選択', support_kicker='必要なときに、お手伝い', privacy_intro='録音、テキスト、サービスへの接続を Kepsley がどのように扱うか。項目ごとに詳しくご案内します。', support_intro='迷ったときに、わかりやすい道しるべを。録音、AI 機能、バックアップなどの使い方をご確認ください。', help='お困りですか？', email='サポートに連絡', email_note='アプリのバージョンと、起きたことをメールでお知らせください。', docs='Kepsley ガイド', section='項目'),
}

def render(lang,kind):
    brand=CONTENT[lang];label=LABELS[lang];doc=SOURCE[lang][kind]
    root='../' if lang=='en' else '../../';asset=root+'assets/'
    canonical='https://www.kepsley.com/'+brand['path']+kind+'/'
    title=doc['title'];description=label[kind+'_intro']
    def languages():
        return ''.join(f'<a href="{root+value["path"]+kind}/" lang="{key}" hreflang="{key}"'+(' aria-current="page"' if key==lang else '')+f'>{value["language"]}</a>' for key,value in CONTENT.items())
    def page_link(target,text):
        return f'<a href="'+('./' if kind==target else '../'+target+'/')+'"'+(' aria-current="page"' if kind==target else '')+f'>{text}</a>'
    page_links=page_link('privacy',brand['privacy'])+page_link('support',brand['support'])
    toc=''.join(f'<a href="#section-{i:02d}"><span>{i:02d}</span>{escape(item["heading"])}</a>' for i,item in enumerate(doc['sections'],1))
    sections='\n'.join(f'<section class="doc-section" id="section-{i:02d}" aria-labelledby="heading-{i:02d}"><span class="section-number" aria-hidden="true">{i:02d}</span><h2 id="heading-{i:02d}">{escape(item["heading"])}</h2>{item["html"]}</section>' for i,item in enumerate(doc['sections'],1))
    alternate=''.join(f'<link rel="alternate" hreflang="{key}" href="https://www.kepsley.com/{value["path"]}{kind}/">' for key,value in CONTENT.items())
    symbol='<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6l-8-3Z"/><path d="m8 12 3 3 5-6"/>' if kind=='privacy' else '<path d="M4 13v-1a8 8 0 0 1 16 0v1M5 12H3v6h4v-6H5Zm14 0h2v6h-4v-6h2Zm0 6c0 3-3 3-7 3"/>'
    hero_symbol=f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{symbol}</svg>'
    contact=f'<a class="contact-button" href="mailto:otsgame@yahoo.com">{label["email"]}{icon("arrow")}</a>'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · Kepsley</title><meta name="description" content="{escape(description,quote=True)}"><meta name="theme-color" content="#081426">
<link rel="canonical" href="{canonical}">{alternate}<link rel="alternate" hreflang="x-default" href="https://www.kepsley.com/{kind}/">
<meta property="og:type" content="website"><meta property="og:site_name" content="Kepsley"><meta property="og:locale" content="{brand['locale']}"><meta property="og:title" content="{escape(title,quote=True)} · Kepsley"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://www.kepsley.com/assets/share.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{asset}mark.svg"><link rel="stylesheet" href="{asset}documents.css">
</head>
<body class="document-page {kind}-page" id="top">
<a class="skip-link" href="#main">{brand['skip']}</a>
<header class="site-header wrap"><a class="wordmark" href="../" aria-label="{brand['back']}"><img src="{asset}mark.svg" width="32" height="32" alt="">Kepsley</a><div class="header-right"><nav class="main-nav" aria-label="{label['breadcrumb']}"><a href="../">{label['home']}</a>{page_links}</nav><details class="languages"><summary aria-label="{brand['lang_label']}">{icon('globe')}{brand['language']}</summary><nav class="language-list" aria-label="{brand['lang_label']}">{languages()}</nav></details></div></header>
<main id="main" class="wrap">
<nav class="breadcrumb" aria-label="{label['breadcrumb']}"><a href="../">{label['home']}</a><span aria-hidden="true">/</span><span aria-current="page">{title}</span></nav>
<div class="document-hero"><div><span class="eyebrow">{label[kind+'_kicker']}</span><h1>{title}</h1><p class="document-intro">{description}</p>{contact if kind=='support' else ''}</div><div class="hero-symbol">{hero_symbol}</div></div>
<details class="mobile-index"><summary>{label['toc']}<span aria-hidden="true">＋</span></summary><nav aria-label="{label['toc']}">{toc}</nav></details>
<div class="document-layout"><aside class="sidebar"><nav class="document-index" aria-label="{label['toc']}"><span class="index-title">{label['toc']}</span>{toc}</nav><div class="sidebar-contact"><span class="contact-heading">{label['help']}</span><a href="mailto:otsgame@yahoo.com">otsgame@yahoo.com ↗</a><p>{label['email_note']}</p></div></aside><article class="document-content" aria-label="{title}">{sections}<div class="document-end"><span>Kepsley · {label['docs']}</span><a href="#top">{label['back']} ↑</a></div></article></div>
<section class="contact-panel" aria-labelledby="contact-title"><div><h2 id="contact-title">{label['help']}</h2><p>{label['email_note']}</p></div><a class="contact-address" href="mailto:otsgame@yahoo.com">otsgame@yahoo.com {icon('arrow')}</a></section>
</main>
<footer class="site-footer wrap"><div class="footer-top"><div class="footer-brand"><a class="wordmark" href="../">Kepsley</a><p>{brand['footer_tag']}</p></div><nav class="footer-links">{page_links}<a href="mailto:otsgame@yahoo.com">{brand['contact']} ↗</a></nav></div><div class="footer-bottom"><span>© 2026 Kepsley · tonyzh</span><nav class="footer-languages" aria-label="{brand['lang_label']}">{languages()}</nav></div></footer>
</body></html>
'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for lang,brand in CONTENT.items():
        for kind in ('privacy','support'):
            path=ROOT/brand['path']/kind/'index.html';value=render(lang,kind)
            if args.check:assert path.read_text()==value, f'Document out of date: {path}'
            else:path.write_text(value)
    print('PASS: six document pages match their original body copy and template' if args.check else 'Rendered six document pages')
if __name__=='__main__':main()
