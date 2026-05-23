#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix broken </div>> and i18n font/animation fallbacks."""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

FONT_LINKS = {
    "en": '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">',
    "ko": '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+KR:wght@400;500;600;700&display=swap">',
    "ja": '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+JP:wght@400;500;600;700&display=swap">',
}

FONT_VARS = {
    "en": "    --font:'Inter','SF Pro Display','Alibaba PuHuiTi 3.0','PingFang SC','Microsoft YaHei',sans-serif;",
    "ko": "    --font:'Inter','Noto Sans KR','SF Pro Display','Apple SD Gothic Neo','Malgun Gothic',sans-serif;",
    "ja": "    --font:'Inter','Noto Sans JP','SF Pro Display','Hiragino Sans','Yu Gothic',sans-serif;",
}

ANIM_FIX = """
  /* i18n: show content even if entrance JS fails */
  html[lang="en"] [data-anim],
  html[lang="ko"] [data-anim],
  html[lang="ja"] [data-anim]{opacity:1;transform:none;}
"""


def lang_from_path(path: str) -> str:
    rel = os.path.relpath(path, ROOT)
    parts = rel.split(os.sep)
    if "en" in parts:
        return "en"
    if "ko" in parts:
        return "ko"
    if "ja" in parts:
        return "ja"
    return "zh"


def iter_html_files():
    for dirpath, _, files in os.walk(ROOT):
        if "_build" in dirpath or ".vercel" in dirpath:
            continue
        for name in files:
            if name.endswith(".html"):
                yield os.path.join(dirpath, name)


def fix_file(path: str):
    lang = lang_from_path(path)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    changed = False
    if "</div>>" in html:
        html = html.replace("</div>>", "</div>")
        changed = True
    if re.search(r"</div>\s+aria-label=", html):
        html = re.sub(r"</div>\s+aria-label=\"[^\"]*\">", "</div>", html)
        changed = True
    if lang != "zh":
        link = FONT_LINKS[lang]
        if "Noto+Sans" not in html and lang in ("ko", "ja"):
            html = html.replace(
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">',
                link,
            )
            changed = True
        if FONT_VARS.get(lang):
            html = re.sub(
                r"    --font:'Inter','SF Pro Display','Alibaba PuHuiTi 3\.0','PingFang SC','Microsoft YaHei',sans-serif;",
                FONT_VARS[lang],
                html,
                count=1,
            )
            changed = True
        if ANIM_FIX.strip() not in html:
            html = html.replace(
                "  [data-anim].in{opacity:1;transform:none;}",
                "  [data-anim].in{opacity:1;transform:none;}" + ANIM_FIX,
                1,
            )
            changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("fixed", os.path.relpath(path, ROOT))


def main():
    for path in sorted(iter_html_files()):
        fix_file(path)


if __name__ == "__main__":
    main()
