"""Shared page chrome, metadata and semantics, applied after translation."""
from pathlib import Path
import re
from _models import render_models

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = 'https://fomo-newbie.vercel.app'
LANGS = {'zh': ('中', '中文'), 'en': ('EN', 'English'), 'ko': ('한', '한국어'), 'ja': ('日', '日本語')}
COPY = {
    'zh': ('选择赛季', '选择语言', '前往产品平台', '返回新手手册', '跳转到正文', '已结束', '9/24 开始', '本赛季已结束，以下保留历史规则。', '查看 S3', '社区指南 · 仅供学习，不构成投资建议。'),
    'en': ('Choose season', 'Choose language', 'Product platforms', 'Back to the guide', 'Skip to content', 'Ended', 'Starts 9/24', 'This season has ended. Historical rules are preserved below.', 'View S3', 'Community guide · For education, not investment advice.'),
    'ja': ('シーズンを選択', '言語を選択', 'プラットフォーム', 'ガイドに戻る', '本文へスキップ', '終了', '9/24開始', 'このシーズンは終了しました。以下は過去のルールです。', 'S3を見る', 'コミュニティガイド · 学習用であり、投資助言ではありません。'),
    'ko': ('시즌 선택', '언어 선택', '제품 플랫폼', '가이드로 돌아가기', '본문으로 건너뛰기', '종료', '9/24 시작', '종료된 시즌입니다. 아래에는 당시 규칙을 보존했습니다.', 'S3 보기', '커뮤니티 가이드 · 학습용이며 투자 조언이 아닙니다.'),
}

def path(page, lang):
    base = '' if page == 'guide' else '/season-' + page[1:]
    return (base + ('' if lang == 'zh' else '/' + lang) + '/')

def icon(name):
    return f'<i data-lucide="{name}" aria-hidden="true"></i>'

def chrome(page, lang):
    season, language, products, back, skip, ended, starts, archive, latest, disclaimer = COPY[lang]
    logo = (ROOT / 'templates/brand.svg').read_text().strip()
    label = 'FOMO · Newbie Guide' if page == 'guide' else 'FOMO · Season ' + page[1:]
    seasons = ''.join(f'<a href="{path(p,lang)}"' + (' aria-current="page"' if p == page else '') + f'><span class="season-tag">S{p[1:]}</span><span class="season-item-body"><span class="season-item-title">Season {p[1:]}<span class="season-status">{starts if p == "s3" else ended}</span></span></span></a>' for p in ('s3','s1','s2'))
    languages = ''.join(f'<a href="{path(page,l)}" lang="{l}" hreflang="{l}"' + (' aria-current="page"' if l == lang else '') + f'>{LANGS[l][1]}</a>' for l in ('en','zh','ko','ja'))
    header = f'''<header class="site-header"><div class="topbar">
<div class="header-left"><a class="brand" href="{path('guide',lang)}" aria-label="FLock.io · {back}">{logo}</a><span class="header-tag">{label}</span><details class="nav-picker"><summary aria-label="{season}">Season {icon('chevron-down')}</summary><nav aria-label="{season}">{seasons}</nav></details></div>
<div class="header-actions" role="group" aria-label="{products}"><details class="nav-picker language-picker"><summary aria-label="{language} · {LANGS[lang][0]}">{LANGS[lang][0]} {icon('chevron-down')}</summary><nav aria-label="{language}">{languages}</nav></details><a class="header-platform" href="https://platform.flock.io" target="_blank" rel="noopener"><span class="label-full">API Platform</span><span class="label-short">API</span>{icon('arrow-up-right')}</a><a class="header-platform header-primary" href="https://fomo.flock.io" target="_blank" rel="noopener">FOMO {icon('arrow-up-right')}</a></div>
</div></header>'''
    footer = (ROOT / 'templates/footer.html').read_text().strip().replace('{{logo}}',logo).replace('{{page_label}}',label)
    footer = footer.replace('</footer>', f'<p class="footer-inner footer-note">{disclaimer}</p></footer>')
    return header, footer

def metadata(html, page, lang):
    head, rest = html.split('</head>', 1)
    head = re.sub(r'<link[^>]*href="https://fonts.googleapis.com/css2\?[^>]*>\s*', '', head)
    head = re.sub(r'<link\b[^>]*rel="(?:canonical|alternate)"[^>]*>\s*', '', head)
    head = re.sub(r'<meta\b[^>]*property="og:url"[^>]*>\s*', '', head)
    url = ORIGIN + path(page,lang)
    head += f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n'
    for l in LANGS:
        head += f'<link rel="alternate" hreflang="{"zh-Hans" if l == "zh" else l}" href="{ORIGIN + path(page,l)}">\n'
    head += f'<link rel="alternate" hreflang="x-default" href="{ORIGIN + path(page,"en")}">\n'
    head = re.sub(r'((?:property="og:image"|name="twitter:image") content=")([^"/][^":]*)(")', lambda m: m[1]+ORIGIN+'/'+m[2]+m[3], head)
    head = re.sub(r'<link[^>]*href="/site.css[^>]*>\s*', '', head)
    head = re.sub(r'<script[^>]*src="/site.js[^>]*></script>\s*', '', head)
    # All locales load the same Latin fonts; CJK fonts and fallback live in site.css.
    if 'fonts.googleapis.com/css2?' not in head:
        head += '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">\n'
    head += '<link rel="stylesheet" href="/site.css?v=20260926">\n<script defer src="/site.js?v=20260926"></script>\n'
    return head + '</head>' + rest

def patch_site(html, page, lang):
    header, footer = chrome(page,lang)
    if '<!-- site-header -->' in html:
        html = html.replace('<!-- site-header -->',header,1)
    else:
        html = re.sub(r'<header\b[^>]*>[\s\S]*?</header>',lambda _:header,html,count=1)
    if '<!-- site-footer -->' in html:
        html = html.replace('<!-- site-footer -->',footer,1)
    else:
        html = re.sub(r'<footer\b[^>]*>[\s\S]*?</footer>',lambda _:footer,html,count=1)
    if '<main' not in html:
        html = html.replace('</header>','</header>\n<main id="main" tabindex="-1">',1).replace('<footer','</main>\n<footer',1)
    html = re.sub(r'<main(?:\s[^>]*)?>', '<main id="main" tabindex="-1">', html, count=1)
    if 'class="skip-link"' not in html:
        html = html.replace('<body>',f'<body>\n<a class="skip-link" href="#main">{COPY[lang][4]}</a>',1)
    if page in ('s1','s2'):
        if '<h1' not in html:
            html = re.sub(r'<h2([^>]*)>([\s\S]*?)</h2>', r'<h1 class="season-heading"\1>\2</h1>', html, count=1)
        html = re.sub(r'\n?<aside class="archive-note"[\s\S]*?</aside>','',html)
        notice = f'<aside class="archive-note"><p>{COPY[lang][7]}</p><a href="{path("s3",lang)}">{COPY[lang][8]} {icon("arrow-right")}</a></aside>'
        html = re.sub(r'(<h1[^>]*>[\s\S]*?</h1>)',lambda m:m[0]+'\n'+notice,html,count=1)
        html = re.sub(r'(<div class="sec-num" data-anim>)(?:09 — )?SEASON [12] · [^<]*(</div>)',lambda m:m[1]+f'SEASON {page[1:]} · {COPY[lang][5]}'+m[2],html,count=1)
    # Link the otherwise orphaned guide slider label after translating its text.
    html = re.sub(r'<label>([^<]*)</label>(\s*<input type="range" id="slider")',r'<label for="slider">\1</label>\2',html)
    html = re.sub(r'<label>([^<]*)</label>(\s*<div class="calc-toggle" id="s1StakeToggle")',r'<span id="stake-label">\1</span>\2',html)
    html = html.replace('id="s1StakeToggle">','id="s1StakeToggle" role="group" aria-labelledby="stake-label">')
    html = re.sub(r'(<button[^>]*data-stake="([01])"[^>]*)(>)',lambda m: re.sub(r' aria-pressed="[^"]*"','',m[1])+f' aria-pressed="{"true" if m[2]=="1" else "false"}">',html)
    if page == 's3':
        html = render_models(html,lang)
    html = metadata(html,page,lang)
    return html
