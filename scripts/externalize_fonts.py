#!/usr/bin/env python3
"""Extract inline base64 Alibaba PuHuiTi fonts to /fonts/*.woff2 and rewrite @font-face."""

from __future__ import annotations

import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = ROOT / "fonts"
SOURCE_FILES = (
    "guide.html",
    "season-1.html",
    "season-2.html",
    "season-2-en.html",
    "season-2-ko.html",
    "season-2-ja.html",
)

FONT_BLOCK = re.compile(
    r"@font-face\{\s*font-family:'Alibaba PuHuiTi 3\.0';\s*"
    r"src:url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)\s*format\('woff2'\);\s*"
    r"font-weight:(\d+);font-style:normal;font-display:swap;\s*"
    r"(unicode-range:[^;]+;\s*)?"
    r"\}",
    re.DOTALL,
)


def font_filename(weight: int, decoded_len: int) -> str:
    suffix = "-subset" if decoded_len < 40_000 else ""
    return f"AlibabaPuHuiTi-{weight}{suffix}.woff2"


def ensure_font_file(filename: str, data: bytes) -> None:
    path = FONTS_DIR / filename
    if not path.exists():
        path.write_bytes(data)
    elif path.read_bytes() != data:
        raise SystemExit(f"Font hash mismatch for {filename}")


def replace_block(match: re.Match[str]) -> str:
    b64, weight_s, unicode_range = match.group(1), match.group(2), match.group(3) or ""
    weight = int(weight_s)
    data = base64.b64decode(b64)
    filename = font_filename(weight, len(data))
    ensure_font_file(filename, data)

    range_line = f"    {unicode_range.strip()}\n" if unicode_range.strip() else ""
    if "\n" in match.group(0)[:60]:
        return (
            f"@font-face{{\n"
            f"    font-family:'Alibaba PuHuiTi 3.0';\n"
            f"    src:url(/fonts/{filename}) format('woff2');\n"
            f"    font-weight:{weight};font-style:normal;font-display:swap;\n"
            f"{range_line}"
            f"  }}"
        )
    range_inline = unicode_range.strip()
    range_part = f"{range_inline}" if range_inline else ""
    return (
        f"@font-face{{font-family:'Alibaba PuHuiTi 3.0';"
        f"src:url(/fonts/{filename}) format('woff2');"
        f"font-weight:{weight};font-style:normal;font-display:swap;"
        f"{range_part}}}"
    )


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    if "data:font/woff2;base64," not in text:
        print(f"{path.name}: already externalized, skip")
        return 0
    new_text, count = FONT_BLOCK.subn(replace_block, text)
    if count != 8:
        raise SystemExit(f"{path.name}: expected 8 @font-face blocks, replaced {count}")
    path.write_text(new_text, encoding="utf-8")
    return count


def main() -> None:
    FONTS_DIR.mkdir(exist_ok=True)
    for name in SOURCE_FILES:
        path = ROOT / name
        if not path.exists():
            raise SystemExit(f"Missing {path}")
        n = process_file(path)
        print(f"{name}: externalized {n} font blocks")
    files = sorted(FONTS_DIR.glob("*.woff2"))
    print(f"fonts/: {len(files)} files")
    for f in files:
        print(f"  {f.name}: {f.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
