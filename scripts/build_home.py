#!/usr/bin/env python3
"""Render three static brand homepages. --check validates generated pages without writing."""
from pathlib import Path
from html import escape
import argparse

ROOT = Path(__file__).resolve().parents[1] / 'site'
APP_STORE_URL = 'https://apps.apple.com/app/id6817633126'
CONTENT = {
'en': dict(path='', locale='en_GB', title='Your personal memory butler · Kepsley', description='Be here. Let Kepsley keep what matters. A little help to capture conversations, gather your thoughts, and return to the moments worth keeping.',
    language='English', skip='Skip to content', nav=['How it helps', 'Everyday moments', 'About'], eyebrow='Your personal memory butler', hero=['Be here.', 'Let Kepsley keep', '<em>what matters.</em>'], intro='The conversations, the little sparks, the things worth remembering. Bring your scattered moments into focus, ready to revisit.', cta='Meet Kepsley', download='Download for iOS', quiet='A little care for the things on your mind.',
    conversation='A conversation', time='Today, 10:30', card_title='The little things<br>we talked about.', card_copy='A shared idea. A detail to come back to.<br>A conversation, thoughtfully gathered.', tag='A moment, kept', idea='What if we<br>tried this…', idea_label='A little spark', postcard='The long way home.', postcard_date='An ordinary day, worth keeping', stamp_top='Little things', stamp_bottom='Kept with care', demo='ILLUSTRATIVE MOMENTS · NOT PERSONAL DATA',
    strip=['Conversations, remembered.', 'Thoughts, gathered.', 'Moments, kept.'], how_kicker='01 / A little help, thoughtfully given', how_title=['Less to hold in your head.', 'More room to be here.'], how_intro='Like a thoughtful butler, Kepsley helps you keep the important details in order. You choose what to record and how to make sense of it.', steps=[('Keep the moment.', 'Capture a conversation or a passing thought before the details fade.'), ('Find the thread.', 'Turn spoken words into text. Use AI to help bring the key points into focus.'), ('Come back to it.', 'Keep things organized, so you can find and revisit what matters to you.')],
    moments_kicker='02 / In the middle of everyday life', moments_title='Not just the big moments.', moments_intro='Small details have a way of becoming the things we want to keep.', scenes=[('An important conversation', 'Be part of the conversation. Keep a record you can return to when you want to remember the details.', '“That’s the part I wanted to remember.”'), ('A passing inspiration', 'An idea on a walk. A thought between meetings. Give it a place before the next thing comes along.', '“What if we tried a different way?”'), ('A memory to come back to', 'A familiar voice, a story, an ordinary afternoon. Keep a little of what made it yours.', '“Tell me that story again.”')], examples='Illustrative scenes and sample words, not customer stories.',
    close_kicker='A little more present. A little less to carry.', close_title='Important things,<br><em>in good hands.</em>', close_copy='Kepsley is your personal memory butler. A thoughtful place for the conversations and ideas you want to keep.', ownership='Your choice of what to record. Your choice of how to organize it.', footer_tag='A little care for what matters.', privacy='Privacy', support='Support', contact='Say hello', back='Kepsley home', lang_label='Choose language'),
'zh-Hans': dict(path='zh/', locale='zh_CN', title='你的私人记忆管家 · Kepsley', description='专注当下，重要的事交给 Kepsley。留住值得记下的对话与灵感，让零散的片段，成为清晰可回顾的记忆。',
    language='简体中文', skip='跳至正文', nav=['管家如何帮你', '日常片段', '关于 Kepsley'], eyebrow='你的私人记忆管家', hero=['专注当下，', '重要的事交给', '<em>Kepsley.</em>'], intro='留住值得记下的对话与灵感，让零散的片段，成为清晰可回顾的记忆。', cta='认识 Kepsley', download='iOS 下载', quiet='细心照料，你放在心上的事。',
    conversation='一段对话', time='今天 · 10:30', card_title='那些聊过的，<br>值得记住的小事。', card_copy='一个共同的想法，一处想回顾的细节。<br>零散的话语，被细心整理。', tag='把这一刻，留下来', idea='如果换个<br>想法呢……', idea_label='灵光一闪', postcard='回家时，多走了一段路。', postcard_date='平常的一天，也值得记下', stamp_top='LITTLE THINGS', stamp_bottom='KEPT WITH CARE', demo='场景示意 · 非真实个人记录',
    strip=['对话，有迹可循。', '灵感，有处安放。', '回忆，留待重温。'], how_kicker='01 / 一位细心的记忆管家', how_title=['脑海少一点负担，', '当下多一份从容。'], how_intro='像一位体贴的管家，Kepsley 帮你照料重要的信息。由你开启记录，也由你选择如何整理。', steps=[('记下重要片段', '一次交谈，一个转瞬即逝的念头。在细节淡去之前，给它留个位置。'), ('理清内容', '把声音转成文字，借助 AI 梳理重点，让散落的想法变得清晰。'), ('留待回顾', '把记录分门别类。需要时，找到那些值得再次读起、听起的片段。')],
    moments_kicker='02 / 陪你留住日常的细节', moments_title='不止是大事，<br>小事也值得被记住。', moments_intro='一些不起眼的瞬间，后来成了我们最想留住的事。', scenes=[('一次重要的交流', '认真倾听眼前的人。想回顾时，再从记录里找回讨论过的细节。', '“这就是我想记住的那句话。”'), ('一个突然的灵感', '散步时的念头，两场会议间的想法。在下一件事到来之前，把它留下。', '“如果，我们换一种方式呢？”'), ('一段想留住的回忆', '熟悉的声音，一个故事，一个平常的下午。留下一点属于你的时刻。', '“那个故事，再讲一次吧。”')], examples='以上为场景与文字示意，并非用户评价或真实个人记录。',
    close_kicker='多一点专注，少一点挂念。', close_title='让重要的事，<br><em>有处安放。</em>', close_copy='Kepsley，你的私人记忆管家。细心整理值得留住的对话与灵感，陪你回顾生活里的重要片段。', ownership='由你决定记录什么，如何整理。', footer_tag='细心照料，重要的小事。', privacy='隐私政策', support='帮助与支持', contact='打个招呼', back='Kepsley 首页', lang_label='选择语言'),
'ja': dict(path='ja/', locale='ja_JP', title='あなたの記憶を大切にする執事 · Kepsley', description='今この瞬間に、心を向けて。大切なことは Kepsley に。残したい会話やひらめきを、いつでも振り返れる記録に整えます。',
    language='日本語', skip='本文へ移動', nav=['できること', '日々のひとこま', 'Kepsley について'], eyebrow='あなたの記憶を大切にする執事', hero=['今この瞬間に。', '大切なことは、', '<em>Kepsley に。</em>'], intro='残しておきたい会話や、ふとしたひらめき。散らばったひとこまを、いつでも振り返れる記録に整えます。', cta='Kepsley を知る', download='iOS版をダウンロード', quiet='心に留めておきたいことを、大切に。',
    conversation='ある日の会話', time='今日 · 10:30', card_title='話したこと。<br>覚えておきたいこと。', card_copy='一緒に考えたアイデア。思い返したい細部。<br>何気ない言葉を、丁寧にまとめて。', tag='このひとときを残す', idea='こんなふうに<br>してみたら…', idea_label='小さなひらめき', postcard='少し遠回りした帰り道。', postcard_date='何気ない一日も、大切に', stamp_top='LITTLE THINGS', stamp_bottom='KEPT WITH CARE', demo='場面のイメージ · 個人の記録ではありません',
    strip=['会話を、記録に。', 'ひらめきに、居場所を。', '思い出を、もう一度。'], how_kicker='01 / さりげなく、丁寧にお手伝い', how_title=['覚える負担を減らして、', '今を楽しむ余白を。'], how_intro='気の利く執事のように、大切な情報を整えるお手伝い。何を記録し、どうまとめるかは、あなたが決められます。', steps=[('大切な瞬間を残す', '会話や、ふと浮かんだ考え。細かなことが薄れる前に、記録として残します。'), ('内容を整える', '声を文字に。AI の力も借りながら、散らばった話の要点を見つけます。'), ('いつでも振り返る', '記録を整理して、必要なときに探せるように。読み返し、聞き返すための場所に。')],
    moments_kicker='02 / 日々の小さな出来事とともに', moments_title='特別な日だけでなく、<br>何気ない瞬間にも。', moments_intro='小さな出来事が、あとから大切な思い出になることがあります。', scenes=[('大切な人との会話', '目の前の相手の話に耳を傾けて。話し合ったことは、あとから記録で振り返れます。', '「この言葉を、覚えておきたかった。」'), ('ふいに生まれるひらめき', '散歩中のアイデアや、仕事の合間の思いつき。次の用事が来る前に、居場所を。', '「違うやり方も、あるかもしれない。」'), ('また触れたい思い出', 'なじみの声、懐かしい話、いつもの午後。あなたらしい時間を、少しだけ残して。', '「あの話を、もう一度聞かせて。」')], examples='場面と言葉は説明用のイメージであり、利用者の体験談や個人の記録ではありません。',
    close_kicker='今に集中する。心の荷物を、少し軽く。', close_title='大切なことに、<br><em>ふさわしい居場所を。</em>', close_copy='Kepsley は、あなたの記憶を大切にする執事。残したい会話やひらめきを、丁寧に整えるお手伝いをします。', ownership='何を記録し、どう整理するかは、あなた次第。', footer_tag='大切な小さなことに、心を配る。', privacy='プライバシー', support='サポート', contact='お問い合わせ', back='Kepsley ホーム', lang_label='言語を選択')
}
ICONS = {
'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18Z"/>',
'arrow':'<path d="M4 12h15m-6-6 6 6-6 6"/>',
'leaf':'<path d="M5 20C3 8 10 3 21 3c0 11-5 18-16 17Zm0 0L16 9"/>',
'voice':'<rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 10v2a7 7 0 0 0 14 0v-2M12 19v3m-4 0h8"/>',
'spark':'<path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5L12 2Z"/>',
'capture':'<rect x="5" y="3" width="14" height="18" rx="3"/><path d="M9 8h6M9 12h6M9 16h3"/>',
'order':'<path d="M4 7h16M4 12h11M4 17h7m6 0 2 2 4-5"/>',
'folder':'<path d="M3 7V5a2 2 0 0 1 2-2h5l3 4h6a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z"/>',
}
def icon(name, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
ARTS = [
'<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><ellipse cx="150" cy="156" rx="94" ry="11" fill="#0A1D34" opacity=".5"/><g transform="rotate(-8 125 85)"><rect x="40" y="25" width="160" height="109" rx="9" fill="#294764"/><path d="m59 134 12 20 8-20" fill="#294764"/><path d="M63 51h106M63 66h80M63 81h95" stroke="#73A8C9" stroke-width="3" stroke-linecap="round"/></g><g transform="rotate(7 212 118)"><rect x="139" y="89" width="119" height="64" rx="8" fill="#247D9C"/><path d="m232 150 10 15 3-17" fill="#247D9C"/><circle cx="167" cy="121" r="4" fill="#B2EEFF"/><circle cx="185" cy="121" r="4" fill="#B2EEFF"/><circle cx="203" cy="121" r="4" fill="#B2EEFF"/></g></svg>',
'<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><ellipse cx="150" cy="159" rx="76" ry="9" fill="#102A40" opacity=".5"/><g transform="rotate(-9 150 90)"><rect x="82" y="15" width="140" height="139" rx="3" fill="#284E67"/><path d="m199 15 23 23h-23V15Z" fill="#386C87"/><path d="M106 108h91M106 123h61" stroke="#73A8C9" stroke-width="2" stroke-linecap="round"/><path d="m151 34 6 18 18 6-18 6-6 18-6-18-18-6 18-6 6-18Z" stroke="#8AEAFF" stroke-width="2"/><path d="M184 47l7-8m-77 39-10 4m56 9 3 8" stroke="#59B5DB" stroke-width="2" stroke-linecap="round"/></g></svg>',
'<svg viewBox="0 0 300 180" fill="none" aria-hidden="true"><ellipse cx="153" cy="158" rx="92" ry="10" fill="#0A1D34" opacity=".5"/><g transform="rotate(7 150 90)"><rect x="58" y="17" width="185" height="143" rx="4" fill="#294764"/><rect x="69" y="28" width="163" height="102" rx="2" fill="#1D405F"/><circle cx="192" cy="51" r="14" fill="#A5EBFF"/><path d="M69 103c39-45 77-24 99-9 23 16 42-12 64-10v46H69Z" fill="#306886"/><path d="M69 117c60-21 86 20 163-10v23H69Z" fill="#1E9ABE"/><path d="M81 144h68" stroke="#89B6D5" stroke-width="2" stroke-linecap="round"/></g></svg>'
]
def render(lang, d):
    base='../' if d['path'] else ''
    asset=base+'assets/'
    canonical='https://www.kepsley.com/'+d['path']
    def languages():
        return ''.join(f'<a href="{base+v["path"] or "./"}" lang="{k}" hreflang="{k}"'+(' aria-current="page"' if k==lang else '')+f'>{v["language"]}</a>' for k,v in CONTENT.items())
    nav=''.join(f'<a href="#{target}">{escape(label)}</a>' for target,label in zip(['how','moments','about'],d['nav']))
    steps=''.join(f'<article class="step"><div class="step-top"><span>0{i+1}</span>{icon(symbol)}</div><h3>{escape(title)}</h3><p>{escape(copy)}</p></article>' for i,((title,copy),symbol) in enumerate(zip(d['steps'],['capture','order','folder'])))
    scenes=''.join(f'<article class="moment"><div class="moment-art">{art}</div><div class="moment-body"><span class="moment-number">0{i+1} / KEPSLEY MOMENTS</span><h3>{escape(title)}</h3><p>{escape(copy)}</p><div class="moment-example">{escape(quote)}</div></div></article>' for i,((title,copy,quote),art) in enumerate(zip(d['scenes'],ARTS)))
    heights=[9,17,12,23,32,18,12,26,37,23,15,30,40,20,12,23,34,18,11,28,36,22,14,25,32,16,9,20,28,17,12,7]
    waveform=''.join(f'<i style="--h:{h}px"></i>' for h in heights)
    alternate=''.join(f'<link rel="alternate" hreflang="{k}" href="https://www.kepsley.com/{v["path"]}">' for k,v in CONTENT.items())
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(d['title'])}</title><meta name="description" content="{escape(d['description'],quote=True)}">
<meta name="theme-color" content="#081426"><link rel="canonical" href="{canonical}">
{alternate}<link rel="alternate" hreflang="x-default" href="https://www.kepsley.com/">
<meta property="og:type" content="website"><meta property="og:site_name" content="Kepsley"><meta property="og:locale" content="{d['locale']}">
<meta property="og:title" content="{escape(d['title'],quote=True)}"><meta property="og:description" content="{escape(d['description'],quote=True)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://www.kepsley.com/assets/share.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Kepsley — {escape(d['eyebrow'],quote=True)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(d['title'],quote=True)}"><meta name="twitter:description" content="{escape(d['description'],quote=True)}"><meta name="twitter:image" content="https://www.kepsley.com/assets/share.png">
<link rel="icon" type="image/svg+xml" href="{asset}mark.svg"><link rel="stylesheet" href="{asset}home.css">
</head>
<body class="home">
<a class="skip-link" href="#main">{d['skip']}</a>
<header class="site-header wrap"><a class="wordmark" href="./" aria-label="{d['back']}"><img src="{asset}mark.svg" width="32" height="32" alt="">Kepsley</a><div class="header-right"><nav class="main-nav" aria-label="{d['back']}">{nav}</nav><details class="languages"><summary aria-label="{d['lang_label']}">{icon('globe')}{d['language']}</summary><nav class="language-list" aria-label="{d['lang_label']}">{languages()}</nav></details></div></header>
<main id="main">
<section class="hero wrap" aria-labelledby="hero-title"><div class="hero-copy fade-in"><div class="eyebrow">{d['eyebrow']}</div><h1 id="hero-title">{''.join('<span>'+line+'</span>' for line in d['hero'])}</h1><p class="hero-intro">{d['intro']}</p><div class="hero-actions"><a class="primary-link" href="#how">{d['cta']}{icon('arrow')}</a><a class="download-link" href="{APP_STORE_URL}">{d['download']}</a></div><p class="quiet-note">{icon('leaf')}{d['quiet']}</p></div>
<div class="memory-scene fade-in" role="img" aria-label="{d['demo']}"><div class="halo" aria-hidden="true"></div><svg class="orbit" viewBox="0 0 550 520" fill="none" aria-hidden="true"><path d="M37 310C-30 145 266-20 435 66c173 88 30 409-173 410-69 1-112-16-139-45" stroke="#2E78A5" stroke-width="1" stroke-dasharray="3 7"/><circle cx="50" cy="159" r="4" fill="#2E78A5"/><path d="m440 256 5 12 12 5-12 5-5 12-5-12-12-5 12-5 5-12Z" fill="#2E78A5"/></svg>
<div class="memory-card conversation-card" aria-hidden="true"><div class="card-top"><span class="card-category">{icon('voice')}{d['conversation']}</span><span>{d['time']}</span></div><h3>{d['card_title']}</h3><div class="waveform">{waveform}</div><div class="card-rule"></div><p class="card-copy">{d['card_copy']}</p><span class="card-tag">{d['tag']}</span></div>
<div class="memory-card idea-card" aria-hidden="true">{icon('spark')}<p>{d['idea']}</p><small>{d['idea_label']}</small></div>
<div class="memory-card postcard" aria-hidden="true"><img src="{asset}memory-landscape.svg" width="400" height="240" alt=""><p>{d['postcard']}</p><small>{d['postcard_date']}</small></div>
<div class="kept-stamp" aria-hidden="true"><span>{d['stamp_top']}</span>{icon('leaf')}<span>{d['stamp_bottom']}</span></div><p class="scene-label">{d['demo']}</p></div></section>
<div class="intro-line wrap" aria-hidden="true"><span>{d['strip'][0]}</span><span class="little-star">✳</span><span>{d['strip'][1]}</span><span class="little-star">✳</span><span>{d['strip'][2]}</span></div>
<section class="section wrap" id="how" aria-labelledby="how-title"><div class="section-heading"><div><span class="section-kicker">{d['how_kicker']}</span><h2 id="how-title">{''.join('<span>'+line+'</span>' for line in d['how_title'])}</h2></div><p>{d['how_intro']}</p></div><div class="steps">{steps}</div></section>
<section class="moments-section" id="moments" aria-labelledby="moments-title"><div class="wrap"><div class="moments-heading"><div><span class="section-kicker">{d['moments_kicker']}</span><h2 id="moments-title">{d['moments_title']}</h2></div><p>{d['moments_intro']}</p></div><div class="moments">{scenes}</div><p class="examples-note">{d['examples']}</p></div></section>
<section class="closing wrap" id="about" aria-labelledby="about-title">{icon('spark','closing-mark')}<span class="section-kicker">{d['close_kicker']}</span><h2 id="about-title">{d['close_title']}</h2><p>{d['close_copy']}</p><p class="ownership">{d['ownership']}</p></section>
</main>
<footer class="site-footer wrap"><div class="footer-top"><div class="footer-brand"><a class="wordmark" href="./">Kepsley</a><p>{d['footer_tag']}</p></div><nav class="footer-links"><a href="privacy/">{d['privacy']}</a><a href="support/">{d['support']}</a><a href="mailto:otsgame@yahoo.com">{d['contact']} ↗</a></nav></div><div class="footer-bottom"><span>© 2026 Kepsley · tonyzh</span><nav class="footer-languages" aria-label="{d['lang_label']}">{languages()}</nav></div></footer>
</body>
</html>
'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for lang,d in CONTENT.items():
        path=ROOT/d['path']/'index.html';html=render(lang,d)
        if args.check:
            assert path.read_text()==html, f'Homepage out of date: {path}; run scripts/build_home.py'
        else:path.write_text(html)
    print('PASS: three static homepages match the source' if args.check else 'Rendered three static homepages')
if __name__=='__main__':main()
