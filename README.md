# FOMO Newbie Guide

Multilingual static handbook for **FOMO** (FLock Open Model Offering): how issuers launch an RMO, how supporters participate, and how bonding curve pricing, anti-sniping tax, graduation, and buyback mechanics work.

**Live site:** [fomo-newbie.vercel.app](https://fomo-newbie.vercel.app) · **Related product:** [fomo.flock.io](https://fomo.flock.io)

| Language | Handbook | Season 1 | Season 2 | Season 3 |
|----------|----------|----------|----------|----------|
| 中文 | [/](https://fomo-newbie.vercel.app/) | [/season-1](https://fomo-newbie.vercel.app/season-1) | [/season-2](https://fomo-newbie.vercel.app/season-2) | [/season-3](https://fomo-newbie.vercel.app/season-3) |
| English | [/en](https://fomo-newbie.vercel.app/en) | [/season-1/en](https://fomo-newbie.vercel.app/season-1/en) | [/season-2/en](https://fomo-newbie.vercel.app/season-2/en) | [/season-3/en](https://fomo-newbie.vercel.app/season-3/en) |
| 한국어 | [/ko](https://fomo-newbie.vercel.app/ko) | [/season-1/ko](https://fomo-newbie.vercel.app/season-1/ko) | [/season-2/ko](https://fomo-newbie.vercel.app/season-2/ko) | [/season-3/ko](https://fomo-newbie.vercel.app/season-3/ko) |
| 日本語 | [/ja](https://fomo-newbie.vercel.app/ja) | [/season-1/ja](https://fomo-newbie.vercel.app/season-1/ja) | [/season-2/ja](https://fomo-newbie.vercel.app/season-2/ja) | [/season-3/ja](https://fomo-newbie.vercel.app/season-3/ja) |

> **Disclaimer:** This handbook is for education only. It does not constitute investment, legal, or tax advice. Token mechanics and parameters on the live platform may change.

---

## Features

- **Static HTML sources** with embedded or shared styles and interactive demos (bonding curve, anti-sniping tax replay, calculators).
- **Four locales** (zh / en / ko / ja); the guide and Season 1 use translation tables, while Seasons 2 and 3 use locale-specific HTML sources.
- **Shared chrome** via `i18n/_header.py`: navigation, hreflang, favicon, and [Vercel Web Analytics](https://vercel.com/docs/analytics) with a custom `Page view by language` event.
- **Clean URLs** on Vercel (`/en`, `/season-1/ko`, …) plus permanent redirects from legacy filenames in `vercel.json`.

---

## Repository layout

```
fomo-newbie/
├── guide.html              # Handbook source (zh) → builds index + i18n variants
├── season-1.html           # Season 1 source (zh)
├── season-2.html           # Season 2 source (zh)
├── season-3*.html          # Season 3 rules sources (zh / en / ko / ja)
├── season-3.css            # Shared Season 3 styles
├── index.html              # Published zh handbook (generated)
├── en/ ko/ ja/             # Published handbook per locale
├── season-1/ season-2/ season-3/  # Published season pages per locale
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
| `season-2*.html` | `season-2/**/index.html` |
| `season-3*.html` | `season-3/**/index.html` |

Do not hand-edit generated `index.html` files under locale folders unless you plan to overwrite them on the next build.

---

## Requirements

- **Python 3.9+** (stdlib only for build scripts)
- **[Vercel CLI](https://vercel.com/docs/cli)** linked to project `fomo-newbie` (optional, for deploy)

---

## Development

```bash
cd fomo-newbie

# 1. Edit source HTML (guide.html, season-1.html, season-2*.html, season-3*.html)
#    and/or translation tables in i18n/guide_*.py, i18n/s1_*.py

# 2. Regenerate all published pages
python3 build_i18n.py
python3 fix_all_headers.py

# 3. Preview locally (any static server), e.g.:
python3 -m http.server 8080
# open http://localhost:8080
```

### Build pipeline

1. **`build_i18n.py`** — Builds the guide and Season 1 from zh sources plus translation tables, publishes locale-specific Season 2 and Season 3 sources, and applies shared header patches (nav, hreflang, favicon, analytics). Staging output under `_build/` is removed after publish.
2. **`fix_all_headers.py`** — Idempotent pass over all 16 published pages if you only changed `_header.py` or analytics snippets.

Season 2 and Season 3 are maintained as locale-specific HTML sources for zh / en / ko / ja. The Season 3 sources publish to `/season-3`, `/season-3/en`, `/season-3/ko`, and `/season-3/ja`.

### Season 3 interactive guide

`season-3.js` shares the accessible tabs, native navigation disclosures and SVG charts across the four S3 sources. Each source contains its localized copy, including a small `s3-copy` JSON block for dynamic explanations. Keep source HTML and published pages in sync with the build above.

The S3 MT-address / API-ID table uses the new S3 IDs. `data/season-3-models.json` records the public FOMO project API sources, addresses, networks and observed IDs checked on 2026-09-23; it is a provenance snapshot, not a build input. Update the four source tables together when mappings change. DSIKH uses the user-provided S3 ID `deepseek-v4.1-flash-dsikh`, while its public project API still reported `deepseek-v4-flash-dsikh` on that date; the table marks this pending platform-field update. ATTN and GOOGLCAT project links include `chain=robinhood`; the other three use `chain=base`.

The staking example fixes usage share at 50% and the gmFLOCK multiplier at 1×, with α = 0.9 or 0.5. The gmFLOCK curve illustrates diminishing returns; it is **not** a wallet-balance calculator or the protocol's exact normalization formula. Scores are not reward amounts.

`season-3-scene.js` loads the pinned, local Three.js 0.186.0 modules from `vendor/three/` only when the reward-pool illustration is visible. Rendering stops when idle or offscreen and respects reduced motion. A static illustration and HTML eligibility labels remain available when WebGL cannot run.

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
