# -*- coding: utf-8 -*-
"""Shared header / lang-switch patches for FOMO i18n pages."""

import re

LANG_META = {
    "en": ("EN", "English"),
    "zh": ("中", "中文"),
    "ko": ("한", "한국어"),
    "ja": ("日", "日本語"),
}
LANG_ORDER = ("en", "zh", "ko", "ja")

VERCEL_ANALYTICS_SNIPPET = (
    '\n<script defer src="/_vercel/insights/script.js"></script>\n'
)

LANG_SWITCH_CSS = """
  .lang-dd{margin-right:6px;position:relative;}
  .lang-dd[data-open="true"]{z-index:120;}
  .lang-dd-btn{min-width:52px;justify-content:center;gap:4px;touch-action:manipulation;-webkit-tap-highlight-color:transparent;}
  .lang-dd[data-open="true"] .hbar-dd-menu{pointer-events:auto;}
  .lang-dd-lbl{font-family:var(--mono);font-size:11px;letter-spacing:0.06em;line-height:1;}
  .lang-dd-menu{min-width:148px;padding:6px;}
  .lang-dd-item{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:9px 10px;border-radius:8px;}
  .lang-dd-item .lang-dd-name{font-size:13px;font-weight:500;color:#fff;}
  .lang-dd-item .lang-dd-code{font-family:var(--mono);font-size:11px;color:rgba(255,255,255,0.5);}
  .lang-dd-item:hover{background:rgba(55,115,255,0.10);}
  .lang-dd-item.is-active{background:rgba(255,255,255,0.08);pointer-events:none;}
  .lang-dd-item.is-active .lang-dd-code{color:rgba(255,255,255,0.85);}
  .hbar-btn .lbl-short{display:none;}
  .hbar-left .hbar-dd#seasonDD,.hbar-actions .lang-dd{flex-shrink:0;}
  @media (max-width:1100px){.htag{display:none;}}
"""

MOBILE_HEADER_GRID = """
    header,.hbar,.hbar-actions{overflow:visible;}
    .hbar-left .hbar-dd#seasonDD{grid-column:2;grid-row:1;justify-self:end;}
    .hbar-actions{grid-template-columns:auto 1fr 1fr;position:relative;z-index:1;}
    .lang-dd{justify-self:start;margin-right:0;position:relative;z-index:5;}
    .lang-dd[data-open="true"]{z-index:120;}
    .hbar-left .hbar-dd#seasonDD .hbar-dd-menu{
      right:0;left:auto;min-width:min(280px,calc(100vw - 32px));z-index:60;
    }
    .lang-dd .hbar-dd-menu{
      left:0;right:auto;min-width:148px;max-width:min(220px,calc(100vw - 24px));z-index:80;
    }
"""

PHONE_LG_CSS = """
  @media (min-width:390px) and (max-width:720px){
    .wrap{padding-left:max(18px,env(safe-area-inset-left));padding-right:max(18px,env(safe-area-inset-right));}
    .hero{padding:60px 0 52px;}
    h1{font-size:clamp(30px,7.2vw,40px);line-height:1.12;margin-bottom:18px;}
    .lede{font-size:17px;line-height:1.65;}
    h2{font-size:clamp(24px,5.8vw,30px);}
    .hbar-actions{gap:10px;}
    .hbar-actions .hbar-btn{font-size:12.5px;padding:10px 10px;}
  }
  @media (min-width:600px) and (max-width:720px){
    .hbar{column-gap:16px;row-gap:12px;}
    .hbar-actions{gap:12px;}
    .hbar svg.logo{max-width:min(160px,36vw);}
  }
"""

OLD_FOCUS_WITHIN_RE = re.compile(
    r"  \.hbar-dd\[data-open=\"true\"\] \.hbar-dd-menu,\n"
    r"  \.hbar-dd:focus-within \.hbar-dd-menu\{opacity:1;pointer-events:auto;transform:translateY\(0\) scale\(1\);\}\n"
    r"  @media \(hover:hover\) and \(pointer:fine\)\{\n"
    r"    \.hbar-dd:hover \.hbar-dd-menu",
    re.MULTILINE,
)

OLD_MOBILE_MENU_RE = re.compile(
    r"    \.hbar-dd-menu\{right:0;left:auto;min-width:min\(280px,calc\(100vw - 32px\)\);\}\n",
    re.MULTILINE,
)

DUPLICATE_MOBILE_GRID_RE = re.compile(
    r"(    header,\.hbar,\.hbar-actions\{overflow:visible;\}\n"
    r"    \.hbar-left \.hbar-dd#seasonDD\{grid-column:2;grid-row:1;justify-self:end;\}\n"
    r"    \.hbar-actions\{grid-template-columns:auto 1fr 1fr;[^\n]+\}\n"
    r"    \.lang-dd\{justify-self:start;margin-right:0;[^\n]+\}\n"
    r"(?:    \.lang-dd\[data-open=\"true\"\]\{z-index:120;\}\n)?"
    r"    \.hbar-left \.hbar-dd#seasonDD \.hbar-dd-menu\{[\s\S]*?\n"
    r"    \.lang-dd \.hbar-dd-menu\{[\s\S]*?\n"
    r"    \})\s*"
    r"    \.hbar-left \.hbar-dd#seasonDD\{grid-column:2;grid-row:1;justify-self:end;\}\n"
    r"    \.hbar-actions\{grid-template-columns:auto 1fr 1fr;\}\n"
    r"    \.lang-dd\{justify-self:start;margin-right:0;[^\n]*\}\n+",
    re.MULTILINE,
)

LANG_DD_JS = """
  // Header — Language dropdown (click toggle; closes Season menu)
  (function(){
    var dd  = document.getElementById('langDD');
    var btn = document.getElementById('langBtn');
    var menu = document.getElementById('langMenu');
    var season = document.getElementById('seasonDD');
    var seasonBtn = document.getElementById('seasonBtn');
    if(!dd || !btn) return;
    var ignoreOutside = false;
    function closeSeason(){
      if(!season || !seasonBtn) return;
      season.dataset.open='false';
      seasonBtn.setAttribute('aria-expanded','false');
    }
    function close(){ dd.dataset.open='false'; btn.setAttribute('aria-expanded','false'); }
    function open(){ closeSeason(); dd.dataset.open='true'; btn.setAttribute('aria-expanded','true'); }
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      ignoreOutside = true;
      (dd.dataset.open==='true') ? close() : open();
      window.setTimeout(function(){ ignoreOutside = false; }, 0);
    });
    if(menu){
      menu.addEventListener('click', function(e){
        e.stopPropagation();
      });
    }
    document.addEventListener('click', function(e){
      if(ignoreOutside) return;
      if(!dd.contains(e.target)) close();
    });
    document.addEventListener('keydown', function(e){
      if(e.key==='Escape') close();
    });
    if(seasonBtn){
      seasonBtn.addEventListener('click', function(){
        if(season && season.dataset.open==='true') close();
      }, true);
    }
    if(season){
      season.addEventListener('click', function(e){
        if(season.dataset.open==='true' && !dd.contains(e.target)) close();
      });
    }
  })();
"""

OLD_LANG_DD_JS_RE = re.compile(
    r"  // Header — Language dropdown \(click toggle[^\n]*\)\n"
    r"  \(function\(\)\{[\s\S]*?getElementById\('langDD'\)[\s\S]*?\}\)\(\);\n",
    re.MULTILINE,
)

OLD_SEASON_DD_FULL_RE = re.compile(
    r"  // Header — Season dropdown \(click toggle[^\n]*\)\n"
    r"  \(function\(\)\{[\s\S]*?getElementById\('seasonDD'\)[\s\S]*?"
    r"dd\.querySelectorAll\('\.hbar-dd-item-soon'\)[\s\S]*?\}\);\n  \}\)\(\);\n",
    re.MULTILINE,
)

OLD_SEASON_DD_COMPACT_RE = re.compile(
    r"  \(function\(\)\{\n    var dd=document\.getElementById\('seasonDD'\);"
    r"[\s\S]*?hbar-dd-item-soon'\)\.forEach\(function\(a\)\{ a\.addEventListener\('click',"
    r"function\(e\)\{ e\.preventDefault\(\); \}\); \}\);\n  \}\)\(\);\n",
    re.MULTILINE,
)

SEASON_DD_JS = """
  // Header — Season dropdown (click toggle + outside click + esc + soon-item guard)
  (function(){
    var dd  = document.getElementById('seasonDD');
    var btn = document.getElementById('seasonBtn');
    if(!dd || !btn) return;
    var langDD = document.getElementById('langDD');
    var langBtn = document.getElementById('langBtn');
    function closeLang(){
      if(!langDD || !langBtn) return;
      langDD.dataset.open='false';
      langBtn.setAttribute('aria-expanded','false');
    }
    function close(){ dd.dataset.open='false'; btn.setAttribute('aria-expanded','false'); }
    function open(){ closeLang(); dd.dataset.open='true'; btn.setAttribute('aria-expanded','true'); }
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      (dd.dataset.open==='true') ? close() : open();
    });
    document.addEventListener('click', function(e){
      if(!dd.contains(e.target)) close();
    });
    document.addEventListener('keydown', function(e){
      if(e.key==='Escape') close();
    });
    dd.querySelectorAll('a.hbar-dd-item[href^="#"]').forEach(function(a){
      a.addEventListener('click', function(){ close(); });
    });
    dd.querySelectorAll('.hbar-dd-item-soon').forEach(function(a){
      a.addEventListener('click', function(e){ e.preventDefault(); });
    });
  })();
"""

OLD_LANG_SWITCH_CSS_RE = re.compile(
    r"\n  \.lang-switch\{[^}]+\}\n"
    r"  \.lang-switch \.ls\{[^}]+\}\n"
    r"  \.lang-switch \.ls:hover\{[^}]+\}\n"
    r"  \.lang-switch \.ls\.on\{[^}]+\}\n"
    r"  @media\(max-width:720px\)\{\.lang-switch \.ls\{[^}]+\}\}\n"
    r"  \.hbar-btn \.lbl-short\{display:none;\}\n",
    re.MULTILINE,
)

OLD_MOBILE_LANG_GRID_RE = re.compile(
    r"    \.lang-switch\{grid-column:2;grid-row:1;justify-self:end;margin-right:0;\}\n"
    r"    \.hbar-dd\{grid-column:3;grid-row:1;\}\n",
    re.MULTILINE,
)


def guide_path(lang: str) -> str:
    return "/" if lang == "zh" else f"/{lang}"


def season_path(season: str, lang: str) -> str:
    base = f"/season-{season}"
    return base if lang == "zh" else f"{base}/{lang}"


PAGE_SPECS = {
    "guide": {
        "page": "guide",
        "htag": "FOMO · Newbie Guide",
        "nav_label": "Go to product platforms",
        "s1_sub": "Real usage · Season 1 Rewards",
        "s2_sub": "Mapped model usage · from 5/25",
        "s2_pill": '<span class="pill">LIVE</span>',
        "s2_href": "/season-2",
        "s2_soon": False,
        "s1_href": "/season-1",
    },
    "s1": {
        "page": "s1",
        "htag": "FOMO · Season 1",
        "nav_label": "Go to product platforms",
        "s1_sub": "Real usage → reward flywheel",
        "s2_sub": "Mapped model usage · from 5/25",
        "s2_pill": '<span class="pill">LIVE</span>',
        "s2_href": "/season-2",
        "s2_soon": False,
        "s1_href": "/season-1",
        "logo_guide": "/",
        "back_guide": "/",
    },
    "s2": {
        "page": "s2",
        "htag": "FOMO · Season 2",
        "nav_label": "Go to product platforms",
        "s1_sub": "Ended · 5/22",
        "s2_sub": "Mapped model usage · from 5/25",
        "s2_pill": '<span class="pill">LIVE</span>',
        "s2_href": "#",
        "s2_soon": False,
        "s1_href": "/season-1",
        "logo_guide": "/",
        "back_guide": "/",
        "s1_ended": True,
    },
}


def hreflang_block(page: str) -> str:
    if page == "guide":
        return """<link rel="alternate" hreflang="zh-Hans" href="/">
<link rel="alternate" hreflang="en" href="/en">
<link rel="alternate" hreflang="ko" href="/ko">
<link rel="alternate" hreflang="ja" href="/ja">
<link rel="alternate" hreflang="x-default" href="/en">
"""
    if page == "s1":
        return """<link rel="alternate" hreflang="zh-Hans" href="/season-1">
<link rel="alternate" hreflang="en" href="/season-1/en">
<link rel="alternate" hreflang="ko" href="/season-1/ko">
<link rel="alternate" hreflang="ja" href="/season-1/ja">
<link rel="alternate" hreflang="x-default" href="/season-1/en">
"""
    return """<link rel="alternate" hreflang="zh-Hans" href="/season-2">
<link rel="alternate" hreflang="en" href="/season-2/en">
<link rel="alternate" hreflang="ko" href="/season-2/ko">
<link rel="alternate" hreflang="ja" href="/season-2/ja">
<link rel="alternate" hreflang="x-default" href="/season-2/en">
"""


def _lang_hrefs(page: str) -> dict:
    if page == "guide":
        return {"zh": "/", "en": "/en", "ko": "/ko", "ja": "/ja"}
    if page == "s1":
        return {
            "zh": "/season-1",
            "en": "/season-1/en",
            "ko": "/season-1/ko",
            "ja": "/season-1/ja",
        }
    return {
        "zh": "/season-2",
        "en": "/season-2/en",
        "ko": "/season-2/ko",
        "ja": "/season-2/ja",
    }


def lang_switch_html(page: str, active: str) -> str:
    hrefs = _lang_hrefs(page)
    short, _name = LANG_META[active]
    items = []
    for code in LANG_ORDER:
        code_short, name = LANG_META[code]
        href = hrefs[code]
        if code == active:
            items.append(
                f'<a class="hbar-dd-item lang-dd-item is-active" href="{href}" '
                f'role="menuitem" aria-current="page">'
                f'<span class="lang-dd-name">{name}</span>'
                f'<span class="lang-dd-code">{code_short}</span></a>'
            )
        else:
            items.append(
                f'<a class="hbar-dd-item lang-dd-item" href="{href}" role="menuitem">'
                f'<span class="lang-dd-name">{name}</span>'
                f'<span class="lang-dd-code">{code_short}</span></a>'
            )
    menu = "".join(items)
    return (
        f'<div class="lang-dd hbar-dd" id="langDD" data-open="false">'
        f'<button type="button" class="hbar-btn hbar-dd-btn lang-dd-btn" id="langBtn" '
        f'aria-label="Language" aria-haspopup="menu" aria-expanded="false" '
        f'aria-controls="langMenu">'
        f'<span class="lang-dd-lbl">{short}</span>'
        f'<i class="chev" data-lucide="chevron-down"></i></button>'
        f'<div class="hbar-dd-menu lang-dd-menu" id="langMenu" role="menu" '
        f'aria-labelledby="langBtn">{menu}</div></div>'
    )


def _patch_lang_dd_js(html: str) -> str:
    if "ignoreOutside" in html:
        return html
    if OLD_LANG_DD_JS_RE.search(html):
        return OLD_LANG_DD_JS_RE.sub(LANG_DD_JS + "\n", html, count=1)
    if "getElementById('langDD')" not in html and "getElementById(\"langDD\")" not in html:
        for anchor, insert in (
            ("})();\n\n  // Entrance reveal", "})();\n" + LANG_DD_JS + "\n  // Entrance reveal"),
            (
                "  })();\n  (function(){\n    var items=document.querySelectorAll('[data-anim]')",
                "  })();\n" + LANG_DD_JS + "\n  (function(){\n    var items=document.querySelectorAll('[data-anim]')",
            ),
        ):
            if anchor in html:
                html = html.replace(anchor, insert, 1)
                break
    return html


def _patch_season_dd_js(html: str) -> str:
    if "function closeLang()" in html and "getElementById('seasonDD')" in html:
        return html
    if OLD_SEASON_DD_FULL_RE.search(html):
        return OLD_SEASON_DD_FULL_RE.sub(SEASON_DD_JS + "\n", html, count=1)
    if OLD_SEASON_DD_COMPACT_RE.search(html):
        return OLD_SEASON_DD_COMPACT_RE.sub(SEASON_DD_JS + "\n", html, count=1)
    return html


def _patch_header_css(html: str) -> str:
    html = OLD_FOCUS_WITHIN_RE.sub(
        "  .hbar-dd[data-open=\"true\"] .hbar-dd-menu{opacity:1;pointer-events:auto;transform:translateY(0) scale(1);}\n"
        "  @media (hover:hover) and (pointer:fine){\n"
        "    .hbar-dd:focus-within .hbar-dd-menu{opacity:1;pointer-events:auto;transform:translateY(0) scale(1);}\n"
        "    .hbar-dd:hover .hbar-dd-menu",
        html,
        count=1,
    )
    html = OLD_MOBILE_MENU_RE.sub("", html)
    html = DUPLICATE_MOBILE_GRID_RE.sub(r"\1", html)
    if ".hbar-actions .lang-dd{flex-shrink:0" not in html:
        needle = ".lang-dd-item.is-active .lang-dd-code{color:rgba(255,255,255,0.85);}"
        if needle in html:
            html = html.replace(
                needle,
                needle
                + "\n  .hbar-left .hbar-dd#seasonDD,.hbar-actions .lang-dd{flex-shrink:0;}"
                + "\n  @media (max-width:1100px){.htag{display:none;}}",
                1,
            )
        elif ".hbar-actions{display:flex" in html:
            html = html.replace(
                ".hbar-actions{display:flex;align-items:center;gap:10px;flex-shrink:0;}",
                ".hbar-actions{display:flex;align-items:center;gap:10px;flex-shrink:0;}"
                "\n  .hbar-left .hbar-dd#seasonDD,.hbar-actions .lang-dd{flex-shrink:0;}"
                "\n  @media (max-width:1100px){.htag{display:none;}}",
                1,
            )
    if "header,.hbar,.hbar-actions{overflow:visible;}" not in html:
        html = html.replace(
            ".hbar-dd{grid-column:2;grid-row:1;justify-self:end;}",
            ".hbar-dd{grid-column:2;grid-row:1;justify-self:end;}" + MOBILE_HEADER_GRID,
            1,
        )
        html = html.replace(
            "display:grid;grid-template-columns:1fr 1fr;gap:8px;",
            "display:grid;grid-template-columns:auto 1fr 1fr;gap:8px;",
            1,
        )
    if "min-width:390px) and (max-width:720px)" not in html:
        html = html.replace(
            "  /* ---------- hero ---------- */",
            PHONE_LG_CSS + "\n  /* ---------- hero ---------- */",
            1,
        )
    return html


def patch_analytics(html: str) -> str:
    if "insights/script.js" in html:
        return html
    if "</body>" in html:
        return html.replace("</body>", VERCEL_ANALYTICS_SNIPPET + "</body>", 1)
    return html


def patch_header_html(html: str, spec: dict, active_lang: str = "zh") -> str:
    page = spec["page"]
    html = _patch_header_css(html)
    if "hreflang=" not in html:
        insert = hreflang_block(page)
        html = html.replace(
            '<meta name="format-detection" content="telephone=no">',
            '<meta name="format-detection" content="telephone=no">\n' + insert,
            1,
        )

    html = OLD_LANG_SWITCH_CSS_RE.sub("\n", html)
    if ".lang-dd{" not in html:
        html = html.replace("</style>", LANG_SWITCH_CSS + "\n</style>", 1)

    html = OLD_MOBILE_LANG_GRID_RE.sub("", html)

    html = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="/">',
        '<link rel="alternate" hreflang="x-default" href="/en">',
        html,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="/season-1">',
        '<link rel="alternate" hreflang="x-default" href="/season-1/en">',
        html,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="/season-2">',
        '<link rel="alternate" hreflang="x-default" href="/season-2/en">',
        html,
    )

    ls = lang_switch_html(page, active_lang)
    lang_block = (
        r'<div class="(?:lang-switch|lang-dd hbar-dd)"[^>]*>[\s\S]*</div>(?=\s*<a class="hbar-btn")'
    )
    if re.search(lang_block, html):
        html = re.sub(lang_block, ls, html, count=1)
    else:
        html = re.sub(
            r'<nav class="hbar-actions"(?:\s+aria-label="[^"]*")?\s*>',
            f'<nav class="hbar-actions" aria-label="{spec["nav_label"]}">\n      {ls}',
            html,
            count=1,
        )

    html = _patch_lang_dd_js(html)
    html = _patch_season_dd_js(html)

    s2_href = spec.get("s2_href", "#")
    if active_lang != "zh" and s2_href and s2_href != "#":
        s2_href = season_path("2", active_lang)
        spec = {**spec, "s2_href": s2_href}

    if s2_href and s2_href != "#":
        html = html.replace(
            '<a class="hbar-dd-item hbar-dd-item-soon" href="#" role="menuitem" aria-disabled="true" tabindex="-1">',
            f'<a class="hbar-dd-item" href="{s2_href}" role="menuitem">',
        )
        html = html.replace(
            '<span class="hbar-dd-title">Season 2 <span class="pill soon">SOON</span></span>',
            f'<span class="hbar-dd-title">Season 2 {spec["s2_pill"]}</span>',
        )
        html = html.replace(
            '<span class="hbar-dd-sub">敬请期待 · TBA</span>',
            f'<span class="hbar-dd-sub">{spec["s2_sub"]}</span>',
        )
        html = html.replace('href="fomo-season-2.html"', f'href="{s2_href}"')
        html = html.replace('href="/season-2.html"', f'href="{s2_href}"')

    s1_href = spec.get("s1_href", "/season-1")
    if active_lang != "zh":
        s1_href = season_path("1", active_lang)
    html = html.replace('href="fomo-season-1.html"', f'href="{s1_href}"')

    if spec.get("s1_ended"):
        html = html.replace(
            '<span class="hbar-dd-title">Season 1 <span class="pill">LIVE</span></span>',
            '<span class="hbar-dd-title">Season 1 <span class="pill ended">ENDED</span></span>',
        )
        html = html.replace(
            '<span class="hbar-dd-sub">真实使用 · Season 1 Rewards</span>',
            f'<span class="hbar-dd-sub">{spec["s1_sub"]}</span>',
        )

    if "logo_guide" in spec:
        guide_href = guide_path(active_lang)
        html = html.replace("fomo-newbie-guide_3.html", guide_href)
        html = html.replace('href="fomo-newbie-guide_May.html"', f'href="{guide_href}"')
        html = html.replace('href="fomo-newbie-guide_May"', f'href="{guide_href}"')
        html = html.replace('href="guide.html"', f'href="{guide_href}"')
        html = html.replace('href="/guide.html"', f'href="{guide_href}"')

    html = patch_analytics(html)
    return html
