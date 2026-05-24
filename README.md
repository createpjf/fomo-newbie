# FOMO Newbie Guide

Multilingual static handbook for **FOMO** (FLock Open Model Offering): how issuers launch an RMO, how supporters participate, and how bonding curve pricing, anti-sniping tax, graduation, and buyback mechanics work.

**Live site:** [fomo-newbie.vercel.app](https://fomo-newbie.vercel.app) · **Related product:** [fomo.flock.io](https://fomo.flock.io)

| Language | Handbook | Season 1 | Season 2 |
|----------|----------|----------|----------|
| 中文 | [/](https://fomo-newbie.vercel.app/) | [/season-1](https://fomo-newbie.vercel.app/season-1) | [/season-2](https://fomo-newbie.vercel.app/season-2) |
| English | [/en](https://fomo-newbie.vercel.app/en) | [/season-1/en](https://fomo-newbie.vercel.app/season-1/en) | [/season-2/en](https://fomo-newbie.vercel.app/season-2/en) |
| 한국어 | [/ko](https://fomo-newbie.vercel.app/ko) | [/season-1/ko](https://fomo-newbie.vercel.app/season-1/ko) | [/season-2/ko](https://fomo-newbie.vercel.app/season-2/ko) |
| 日本語 | [/ja](https://fomo-newbie.vercel.app/ja) | [/season-1/ja](https://fomo-newbie.vercel.app/season-1/ja) | [/season-2/ja](https://fomo-newbie.vercel.app/season-2/ja) |

> **Disclaimer:** This handbook is for education only. It does not constitute investment, legal, or tax advice. Token mechanics and parameters on the live platform may change.

---

## Features

- **Single-file HTML sources** with embedded styles, fonts, and interactive demos (bonding curve, anti-sniping tax replay, calculators).
- **Four locales** (zh / en / ko / ja) generated from shared sources and translation tables.
- **Shared chrome** via `i18n/_header.py`: navigation, hreflang, favicon, and [Vercel Web Analytics](https://vercel.com/docs/analytics) with a custom `Page view by language` event.
- **Clean URLs** on Vercel (`/en`, `/season-1/ko`, …) plus permanent redirects from legacy filenames in `vercel.json`.

---

## Repository layout

```
fomo-newbie/
├── guide.html              # Handbook source (zh) → builds index + i18n variants
├── season-1.html           # Season 1 source (zh)
├── season-2.html           # Season 2 source (zh)
├── index.html              # Published zh handbook (generated)
├── en/ ko/ ja/             # Published handbook per locale
├── season-1/ season-2/     # Published season pages per locale
├── i18n/                   # Translation modules + header/analytics patches
├── build_i18n.py           # Build pipeline
├── fix_all_headers.py      # Re-apply header/favicon/analytics to all pages
├── fix_html_bugs.py        # One-off HTML repair utilities
├── vercel.json             # Legacy URL redirects
├── favicon.svg             # Site icon (aligned with fomo.flock.io)
├── og-fomo-guide.jpg       # Open Graph image
└── archive/                # Local drafts & snapshots (not deployed, gitignored)
```

### Source vs published files

| Edit these | Output |
|------------|--------|
| `guide.html` | `index.html`, `en/index.html`, `ko/index.html`, `ja/index.html` |
| `season-1.html` | `season-1/**/index.html` |
| `season-2.html` | `season-2/**/index.html` |

Do not hand-edit generated `index.html` files under locale folders unless you plan to overwrite them on the next build.

---

## Requirements

- **Python 3.9+** (stdlib only for build scripts)
- **[Vercel CLI](https://vercel.com/docs/cli)** linked to project `fomo-newbie` (optional, for deploy)

---

## Development

```bash
cd fomo-newbie

# 1. Edit source HTML (guide.html, season-1.html, season-2.html)
#    and/or translation tables in i18n/guide_*.py, i18n/s1_*.py

# 2. Regenerate all published pages
python3 build_i18n.py
python3 fix_all_headers.py

# 3. Preview locally (any static server), e.g.:
python3 -m http.server 8080
# open http://localhost:8080
```

### Build pipeline

1. **`build_i18n.py`** — Reads zh sources, applies string replacements per locale, runs `patch_header_html()` (nav, hreflang, favicon, analytics), writes published paths. Staging output under `_build/` is removed after publish.
2. **`fix_all_headers.py`** — Idempotent pass over all 12 published pages if you only changed `_header.py` or analytics snippets.

Season 2 English/Korean/Japanese builds are skipped until matching staging files exist (`fomo-season-2-en.html`, etc.); zh and any existing locale files still publish.

---

## Deployment

Production is hosted on **Vercel** (static output, no framework build step).

```bash
vercel --prod --yes
```

Ensure [Vercel Web Analytics](https://vercel.com/docs/analytics) is enabled for the project. Language breakdown appears under **Analytics → Events** (`Page view by language`, property `lang`).

---

## Analytics

Each page loads `/_vercel/insights/script.js` and sends:

- Standard page views (by path, e.g. `/`, `/en`, `/season-1/ko`)
- Custom event **`Page view by language`** with `lang`: `zh` | `en` | `ko` | `ja`

Implementation lives in `i18n/_header.py` (`VERCEL_ANALYTICS_SNIPPET`, `patch_analytics()`).

---

## Archive folder

`archive/` holds earlier prototypes and downloaded HTML snapshots. It is **gitignored** and **not deployed**. Safe to keep for reference; changes there do not affect the live site.

---

## Contributing

1. Fork and branch from `main`.
2. Change **source** HTML or `i18n/*.py` translation tables.
3. Run `python3 build_i18n.py` and `python3 fix_all_headers.py`.
4. Open a PR with a short summary and, if UI changed, which locales you verified.

---

## License

- **Source code** in this repository (HTML, Python build tooling) is licensed under the [MIT License](LICENSE).
- **FLock** name, logos, and product copy are trademarks of their respective owners. This repository is a community-maintained handbook site and is not an official FLock corporate repo unless stated otherwise by FLock.io.

---

## Links

| Resource | URL |
|----------|-----|
| Production handbook | https://fomo-newbie.vercel.app |
| FOMO platform | https://fomo.flock.io |
| FLock API Platform | https://platform.flock.io |
| GitHub | https://github.com/createpjf/fomo-newbie |
