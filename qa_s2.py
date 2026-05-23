#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "i18n"))

from _header import patch_header_html, PAGE_SPECS, MOBILE_LANG_GRID  # noqa: E402
from s2_qa import S2_LINKS, S2_EN_EXTRA, S2_KO_EXTRA, S2_JA_EXTRA  # noqa: E402

LAYOUT = {
    "zh": "season-2/index.html",
    "en": "season-2/en/index.html",
    "ko": "season-2/ko/index.html",
    "ja": "season-2/ja/index.html",
}

LEGACY = [
    ("fomo-newbie-guide_May.html", "guide"),
    ("fomo-newbie-guide_May-en.html", "guide"),
    ("fomo-newbie-guide_May-ko.html", "guide"),
    ("fomo-newbie-guide_May-ja.html", "guide"),
    ("fomo-season-1.html", "s1"),
    ("fomo-season-1-en.html", "s1"),
    ("fomo-season-1-ko.html", "s1"),
    ("fomo-season-1-ja.html", "s1"),
    ("fomo-season-2.html", "s2"),
    ("fomo-season-2-en.html", "s2"),
    ("fomo-season-2-ko.html", "s2"),
    ("fomo-season-2-ja.html", "s2"),
]


def apply_pairs(html, pairs):
    for a, b in pairs:
        html = html.replace(a, b)
    return html


def fix_s2(lang, extra):
    path = os.path.join(ROOT, LAYOUT[lang])
    links = S2_LINKS.get(lang, {"guide": "/", "s1": "/season-1", "s2": "/season-2"})
    with open(path, encoding="utf-8") as f:
        html = f.read()
    for old, key in LEGACY:
        html = html.replace(old, links[key])
    if lang != "zh":
        html = apply_pairs(html, extra)
    html = patch_header_html(html, PAGE_SPECS["s2"], lang)
    if MOBILE_LANG_GRID.strip() not in html:
        html = html.replace(
            ".hbar-dd{grid-column:2;grid-row:1;justify-self:end;}",
            ".hbar-dd{grid-column:2;grid-row:1;justify-self:end;}" + MOBILE_LANG_GRID,
            1,
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("fixed", path)


def main():
    fix_s2("zh", [])
    fix_s2("en", S2_EN_EXTRA)
    fix_s2("ko", S2_KO_EXTRA)
    fix_s2("ja", S2_JA_EXTRA)


if __name__ == "__main__":
    main()
