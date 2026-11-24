#!/usr/bin/env python3
"""
Build ONE self-contained HTML file (dist/arkagrid-demo.html) that runs the whole
dashboard + 3D campus with no backend: the browser simulation, the on-device
anomaly detector and the three.js scene (loaded from a CDN).

Use it for static hosting (Netlify Drop, GitHub Pages, Cloudflare Pages, S3...).

    python build_demo.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
html = (ROOT / "index.html").read_text(encoding="utf-8")
css = (ROOT / "style.css").read_text(encoding="utf-8")
app = (ROOT / "app.js").read_text(encoding="utf-8")
campus = (ROOT / "campus3d.js").read_text(encoding="utf-8")

THREE = "https://cdn.jsdelivr.net/npm/three@0.170.0/"
FONTS = ("https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700"
         "&family=Space+Grotesk:wght@400;500;600;700&display=swap")

def safe(js: str) -> str:
    return js.replace("</script", "<\\/script")

# 1. CSS: drop the @import (replaced by a <link>) and inline the rest
css = re.sub(r"@import url\([^)]*\);\s*", "", css, count=1)

# 2. swap the local/CDN import-map bootstrap for a static CDN import map
html = re.sub(
    r"<!-- THREE\.JS IMPORT MAP.*?</script>",
    '<script type="importmap">{"imports":{"three":"%sbuild/three.module.js",'
    '"three/addons/":"%sexamples/jsm/"}}</script>\n'
    '    <script>window.__THREE_SOURCE = "CDN";</script>' % (THREE, THREE),
    html, count=1, flags=re.S)

# 3. inline stylesheet (+ font link), remove external script tags
html = html.replace('<link rel="stylesheet" href="style.css">',
                    '<link rel="stylesheet" href="%s">\n    <style>\n%s\n    </style>' % (FONTS, css))
html = html.replace('<script src="app.js" defer></script>', "")
html = html.replace('<script type="module" src="campus3d.js"></script>', "")

# 4. phones: draw edge to edge and keep content clear of system bars
html = html.replace('content="width=device-width, initial-scale=1.0"',
                    'content="width=device-width, initial-scale=1, viewport-fit=cover"')
html = html.replace("</style>", ":root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);"
                    "padding-bottom:env(safe-area-inset-bottom,0px)}\n</style>", 1)

# 5. inline the app, flagged as standalone (no /api calls)
inline = ("<script>window.ARKAGRID_STANDALONE = true;</script>\n"
          "<script>\n%s\n</script>\n<script type=\"module\">\n%s\n</script>\n</body>") % (safe(app), safe(campus))
html = html.replace("</body>", inline, 1)

out = ROOT / "dist" / "arkagrid-demo.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"Built {out.relative_to(ROOT)}  ({out.stat().st_size / 1024:.0f} KB)")
