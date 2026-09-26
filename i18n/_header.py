# -*- coding: utf-8 -*-
"""Shared header / lang-switch patches for FOMO i18n pages."""

VERCEL_VA_QUEUE = """<script>
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
</script>
"""

VERCEL_INSIGHTS_SCRIPT = '<script defer src="/_vercel/insights/script.js"></script>'

VERCEL_LANG_EVENT_JS = """<script>
(function(){
  function detectLang(){
    var parts = location.pathname.replace(/\\/$/,'').split('/').filter(Boolean);
    var langs = {en:1,ko:1,ja:1};
    for (var i = parts.length - 1; i >= 0; i--) {
      if (langs[parts[i]]) return parts[i];
    }
    return 'zh';
  }
  function trackLang(){
    va('event', {
      name: 'Page view by language',
      data: { lang: detectLang(), page: location.pathname || '/' }
    });
  }
  if (document.readyState === 'complete') trackLang();
  else window.addEventListener('load', trackLang);
})();
</script>
"""

FAVICON_LINK = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'

VERCEL_ANALYTICS_SNIPPET = (
    "\n" + VERCEL_VA_QUEUE + VERCEL_INSIGHTS_SCRIPT + "\n" + VERCEL_LANG_EVENT_JS + "\n"
)

LANG_EVENT_MARKER = "Page view by language"

def patch_favicon(html: str) -> str:
    if 'rel="icon"' in html and "favicon" in html:
        return html
    insert_after = '<meta name="format-detection" content="telephone=no">'
    if insert_after in html:
        return html.replace(
            insert_after,
            insert_after + "\n" + FAVICON_LINK,
            1,
        )
    if "<head>" in html:
        return html.replace("<head>", "<head>\n" + FAVICON_LINK, 1)
    return html


def patch_analytics(html: str) -> str:
    if LANG_EVENT_MARKER in html:
        return html
    if "insights/script.js" not in html:
        if "</body>" in html:
            return html.replace("</body>", VERCEL_ANALYTICS_SNIPPET + "</body>", 1)
        return html
    if "window.va = window.va" not in html:
        html = html.replace(
            '<script defer src="/_vercel/insights/script.js"></script>',
            VERCEL_VA_QUEUE + VERCEL_INSIGHTS_SCRIPT,
            1,
        )
    if LANG_EVENT_MARKER not in html and "</body>" in html:
        html = html.replace("</body>", "\n" + VERCEL_LANG_EVENT_JS + "\n</body>", 1)
    return html


# Kept as the stable public entry point for both build scripts.
from _site import patch_site, path

PAGE_SPECS = {page: {"page": page} for page in ("guide", "s1", "s2", "s3")}

def patch_header_html(html: str, spec: dict, active_lang: str = "zh") -> str:
    page = spec["page"]
    # Normalize legacy guide/season filenames in historical content.
    legacy = {"fomo-newbie-guide_3.html": "guide", "fomo-newbie-guide_May.html": "guide", "guide.html": "guide", "fomo-season-1.html": "s1", "fomo-season-2.html": "s2"}
    for filename, target in legacy.items():
        for prefix in ("", "/"):
            html = html.replace('href="' + prefix + filename + '"', 'href="' + path(target,active_lang) + '"')
    return patch_analytics(patch_favicon(patch_site(html,page,active_lang)))
