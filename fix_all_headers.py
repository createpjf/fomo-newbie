#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-apply header patches to all published HTML paths."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "i18n"))
from _header import patch_header_html, PAGE_SPECS  # noqa: E402

ORPHAN = re.compile(r"</div>\s+aria-label=\"[^\"]*\">")
DOUBLE_GT = re.compile(r"</div>>")

PAGES = [
    ("index.html", "guide", "zh"),
    ("en/index.html", "guide", "en"),
    ("ko/index.html", "guide", "ko"),
    ("ja/index.html", "guide", "ja"),
    ("season-1/index.html", "s1", "zh"),
    ("season-1/en/index.html", "s1", "en"),
    ("season-1/ko/index.html", "s1", "ko"),
    ("season-1/ja/index.html", "s1", "ja"),
    ("season-2/index.html", "s2", "zh"),
    ("season-2/en/index.html", "s2", "en"),
    ("season-2/ko/index.html", "s2", "ko"),
    ("season-2/ja/index.html", "s2", "ja"),
]


def main():
    for rel, key, lang in PAGES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print("skip", rel)
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        html = ORPHAN.sub("</div>", html)
        html = DOUBLE_GT.sub("</div>", html)
        html = patch_header_html(html, PAGE_SPECS[key], lang)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("ok", rel)


if __name__ == "__main__":
    main()
