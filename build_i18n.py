#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build FOMO handbook + S1 localized HTML and publish clean URL layout."""

import importlib.util
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "i18n"))

from _header import patch_header_html, PAGE_SPECS  # noqa: E402

BUILD_DIR = os.path.join(ROOT, "_build")

GUIDE_LAYOUT = {
    "zh": ("index.html", ""),
    "en": ("en/index.html", "/en"),
    "ko": ("ko/index.html", "/ko"),
    "ja": ("ja/index.html", "/ja"),
}

S1_LAYOUT = {
    "zh": ("season-1/index.html", "/season-1"),
    "en": ("season-1/en/index.html", "/season-1/en"),
    "ko": ("season-1/ko/index.html", "/season-1/ko"),
    "ja": ("season-1/ja/index.html", "/season-1/ja"),
}

S2_LAYOUT = {
    "zh": ("season-2/index.html", "/season-2"),
    "en": ("season-2/en/index.html", "/season-2/en"),
    "ko": ("season-2/ko/index.html", "/season-2/ko"),
    "ja": ("season-2/ja/index.html", "/season-2/ja"),
}


def load_replacements(module_name: str):
    path = os.path.join(ROOT, "i18n", f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    reps = list(mod.REPLACEMENTS)
    reps.sort(key=lambda x: len(x[0]), reverse=True)
    return reps


def apply_replacements(html: str, replacements) -> str:
    for old, new in replacements:
        if old in html:
            html = html.replace(old, new)
    return html


def fix_absolute_assets(html: str, out_path: str) -> str:
    """Root-absolute paths for assets when HTML lives in subdirectories."""
    depth = out_path.count("/")
    if depth == 0:
        return html
    # favicon / local static
    html = re.sub(r'href="favicon\.svg"', 'href="/favicon.svg"', html)
    html = re.sub(r'src="favicon\.svg"', 'src="/favicon.svg"', html)
    return html


def build_page(src: str, dst: str, replacements, page_key: str, lang: str):
    with open(src, "r", encoding="utf-8") as f:
        html = f.read()
    html = apply_replacements(html, replacements)
    spec = dict(PAGE_SPECS[page_key])
    html = patch_header_html(html, spec, lang)
    html = fix_absolute_assets(html, dst)
    os.makedirs(os.path.dirname(os.path.join(ROOT, dst)) or ROOT, exist_ok=True)
    out = os.path.join(ROOT, dst)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  wrote {dst} ({len(html)} bytes)")


def publish_from_build(staging: str, layout_map: dict, lang: str):
    rel, _ = layout_map[lang]
    src = os.path.join(BUILD_DIR, staging)
    dst = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(dst) or ROOT, exist_ok=True)
    shutil.copy2(src, dst)


def clean_legacy_deploy_files():
    import glob as g

    for pat in ("fomo-newbie-guide_May*.html", "fomo-season-1*.html", "fomo-season-2*.html"):
        for path in g.glob(os.path.join(ROOT, pat)):
            os.remove(path)
            print("removed legacy", os.path.basename(path))


def main():
    os.chdir(ROOT)
    if os.path.isdir(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR, exist_ok=True)

    # --- Guide (zh + i18n) ---
    print("Building guide zh → index...")
    with open("guide.html", encoding="utf-8") as f:
        zh = f.read()
    zh = patch_header_html(zh, PAGE_SPECS["guide"], "zh")
    zh = fix_absolute_assets(zh, "index.html")
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(zh)

    jobs = [
        ("guide.html", "guide-en.html", "guide_en", "guide", "en"),
        ("guide.html", "guide-ko.html", "guide_ko", "guide", "ko"),
        ("guide.html", "guide-ja.html", "guide_ja", "guide", "ja"),
        ("season-1.html", "season-1-en.html", "s1_en", "s1", "en"),
        ("season-1.html", "season-1-ko.html", "s1_ko", "s1", "ko"),
        ("season-1.html", "season-1-ja.html", "s1_ja", "s1", "ja"),
    ]
    for src, staging, mod, page_key, lang in jobs:
        print(f"Building {staging}...")
        reps = load_replacements(mod)
        build_page(src, os.path.join("_build", staging), reps, page_key, lang)

    publish_from_build("guide-en.html", GUIDE_LAYOUT, "en")
    publish_from_build("guide-ko.html", GUIDE_LAYOUT, "ko")
    publish_from_build("guide-ja.html", GUIDE_LAYOUT, "ja")

    publish_from_build("season-1-en.html", S1_LAYOUT, "en")
    publish_from_build("season-1-ko.html", S1_LAYOUT, "ko")
    publish_from_build("season-1-ja.html", S1_LAYOUT, "ja")

    print("Building season-1 zh...")
    with open("season-1.html", encoding="utf-8") as f:
        s1 = f.read()
    s1 = patch_header_html(s1, PAGE_SPECS["s1"], "zh")
    s1 = fix_absolute_assets(s1, "season-1/index.html")
    os.makedirs(os.path.join(ROOT, "season-1"), exist_ok=True)
    with open(os.path.join(ROOT, "season-1/index.html"), "w", encoding="utf-8") as f:
        f.write(s1)

    print("Building season-2 zh...")
    with open("season-2.html", encoding="utf-8") as f:
        s2 = f.read()
    s2 = patch_header_html(s2, PAGE_SPECS["s2"], "zh")
    s2 = fix_absolute_assets(s2, "season-2/index.html")
    os.makedirs(os.path.join(ROOT, "season-2"), exist_ok=True)
    with open(os.path.join(ROOT, "season-2/index.html"), "w", encoding="utf-8") as f:
        f.write(s2)

    from i18n.s2_qa import S2_EN_EXTRA, S2_KO_EXTRA, S2_JA_EXTRA  # noqa: E402

    S2_LINKS = {
        "en": {"guide": "/en", "s1": "/season-1/en", "s2": "/season-2/en"},
        "ko": {"guide": "/ko", "s1": "/season-1/ko", "s2": "/season-2/ko"},
        "ja": {"guide": "/ja", "s1": "/season-1/ja", "s2": "/season-2/ja"},
    }
    LEGACY_LINKS = [
        ("fomo-newbie-guide_May.html", "guide"),
        ("fomo-newbie-guide_May-en.html", "guide"),
        ("fomo-newbie-guide_May-ko.html", "guide"),
        ("fomo-newbie-guide_May-ja.html", "guide"),
        ("fomo-newbie-guide_May", "guide"),
        ("fomo-season-1.html", "s1"),
        ("fomo-season-1-en.html", "s1"),
        ("fomo-season-1-ko.html", "s1"),
        ("fomo-season-1-ja.html", "s1"),
        ("fomo-season-2.html", "s2"),
        ("fomo-season-2-en.html", "s2"),
        ("fomo-season-2-ko.html", "s2"),
        ("fomo-season-2-ja.html", "s2"),
    ]

    def publish_s2(lang: str, extra: list):
        src_name = "season-2.html" if lang == "zh" else f"season-2-{lang}.html"
        if not os.path.exists(src_name):
            print(f"skip s2 {lang}: missing {src_name}")
            return
        rel = S2_LAYOUT[lang][0]
        with open(src_name, encoding="utf-8") as f:
            html = f.read()
        links = (
            {"guide": "/", "s1": "/season-1", "s2": "/season-2"}
            if lang == "zh"
            else S2_LINKS[lang]
        )
        for old, key in LEGACY_LINKS:
            html = html.replace(old, links[key])
        html = html.replace('href="guide.html"', links["guide"])
        for a, b in extra:
            html = html.replace(a, b)
        html = patch_header_html(html, PAGE_SPECS["s2"], lang)
        html = fix_absolute_assets(html, rel)
        dst = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(dst) or ROOT, exist_ok=True)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  wrote {rel}")

    publish_s2("en", S2_EN_EXTRA)
    publish_s2("ko", S2_KO_EXTRA)
    publish_s2("ja", S2_JA_EXTRA)

    clean_legacy_deploy_files()
    if os.path.isdir(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    print("Done.")


if __name__ == "__main__":
    main()
