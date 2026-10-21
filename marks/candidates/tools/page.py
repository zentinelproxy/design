"""Write marks/candidates/index.html: source raster vs each candidate at
512/128/48/32/16 px on the dark and light grounds.

usage: python page.py <repo-root>

The one-colour marks and the favicon are inlined as <symbol>s so their
currentColor (and the favicon's per-scheme colour) can be set per tile; an
<img> would follow the OS colour scheme, not the tile's ground.
"""

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
C = ROOT / "marks/candidates"
SIZES = [512, 128, 48, 32, 16]


def kb(p):
    return f"{p.stat().st_size / 1024:.1f} KB"


def symbol(file, sid):
    s = (C / file).read_text()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    inner = re.sub(r"<!--.*?-->|<title>.*?</title>|<style>.*?</style>", "", inner, flags=re.S)
    return f'<symbol id="{sid}" viewBox="{vb}">{inner}</symbol>'


symbols = "".join(
    [
        symbol("zentinel-mark-mono-line.svg", "s-line"),
        symbol("zentinel-mark-mono-solid.svg", "s-solid"),
        symbol("favicon.svg", "s-fav"),
    ]
)

ROWS = [
    ("Source raster", "marks/mark/zentinel-mark-disc-512.png (PNG, reference)", ("img", "../mark/zentinel-mark-disc-512.png"), C.parent / "mark/zentinel-mark-disc-512.png"),
    ("Full colour", "zentinel-mark-colour.svg (vtracer)", ("img", "zentinel-mark-colour.svg"), C / "zentinel-mark-colour.svg"),
    ("One colour, line", "zentinel-mark-mono-line.svg (potrace, currentColor)", ("use", "s-line", "ink"), C / "zentinel-mark-mono-line.svg"),
    ("One colour, solid", "zentinel-mark-mono-solid.svg (potrace, currentColor)", ("use", "s-solid", "ink"), C / "zentinel-mark-mono-solid.svg"),
    ("Favicon, one colour", "favicon.svg (orange-700 on light, orange-400 on dark via prefers-color-scheme)", ("use", "s-fav", "fav"), C / "favicon.svg"),
    ("Favicon, colour", "favicon-colour.svg (four flat colours, no media query)", ("img", "favicon-colour.svg"), C / "favicon-colour.svg"),
    ("Current favicon", "marks/source/favicon.png (32 px raster, reference)", ("img", "../source/favicon.png"), C.parent / "source/favicon.png"),
]


def tile(kind, s):
    if kind[0] == "img":
        return f'<img src="{kind[1]}" width="{s}" height="{s}" alt="" loading="lazy">'
    return f'<svg class="{kind[2]}" width="{s}" height="{s}" aria-hidden="true"><use href="#{kind[1]}"/></svg>'


def ground(theme):
    rows = []
    for name, desc, kind, path in ROWS:
        cells = "".join(f'<figure>{tile(kind, s)}<figcaption>{s}</figcaption></figure>' for s in SIZES)
        rows.append(
            f'<div class="row"><div class="label"><b>{name}</b><span>{desc}</span><span>{kb(path)}</span></div>'
            f'<div class="tiles">{cells}</div></div>'
        )
    return f'<section class="ground {theme}"><h2>On the {theme} ground</h2>{"".join(rows)}</section>'


lock = []
for theme in ("dark", "light"):
    interim = C.parent / f"lockup/zentinel-lockup-{theme}.svg"
    cand = C / f"zentinel-lockup-{theme}.svg"
    lock.append(
        f'<section class="ground {theme}"><h2>Lockup on {theme}</h2>'
        f'<div class="lock"><span>interim, raster disc ({kb(interim)})</span>'
        f'<img src="../lockup/zentinel-lockup-{theme}.svg" alt="Zentinel" height="104"><img src="../lockup/zentinel-lockup-{theme}.svg" alt="" height="52"><img src="../lockup/zentinel-lockup-{theme}.svg" alt="" height="28"></div>'
        f'<div class="lock"><span>candidate, vector disc ({kb(cand)})</span>'
        f'<img src="zentinel-lockup-{theme}.svg" alt="Zentinel" height="104"><img src="zentinel-lockup-{theme}.svg" alt="" height="52"><img src="zentinel-lockup-{theme}.svg" alt="" height="28"></div>'
        "</section>"
    )

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shisa trace candidates</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>
:root {{ --page:#f3edf2; --text:#1f161e; --muted:#695c67; --rule:#e4dde3; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --page:#1f161e; --text:#f3edf2; --muted:#aca0ab; --rule:#352934; }} }}
:root[data-theme="dark"] {{ --page:#1f161e; --text:#f3edf2; --muted:#aca0ab; --rule:#352934; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; padding:24px 16px 64px; background:var(--page); color:var(--text);
  font:15px/1.5 "Atkinson Hyperlegible Next", system-ui, -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width:1240px; margin:0 auto; }}
h1 {{ font-size:1.6rem; margin:0 0 .25rem; }}
.warn {{ border-left:4px solid #f68d31; padding:.5rem .9rem; margin:1rem 0 1.5rem; max-width:72ch; }}
p {{ max-width:72ch; color:var(--muted); }}
.ground {{ border-radius:16px; padding:16px; margin:0 0 24px; }}
.ground.dark {{ background:#160d15; color:#faf6fa; --ink:#faf6fa; --fav:#f68d31; --cap:#aca0ab; }}
.ground.light {{ background:#faf6fa; color:#160d15; --ink:#160d15; --fav:#9b4804; --cap:#695c67; border:1px solid var(--rule); }}
.ground h2 {{ font-size:1.05rem; margin:0 0 12px; }}
.row {{ border-top:1px solid color-mix(in srgb, var(--cap) 30%, transparent); padding:12px 0; }}
.label {{ display:flex; flex-wrap:wrap; gap:.25rem 1rem; margin-bottom:8px; font-size:.875rem; }}
.label span {{ color:var(--cap); }}
.tiles {{ display:flex; align-items:flex-end; gap:20px; overflow-x:auto; padding-bottom:4px; }}
figure {{ margin:0; display:flex; flex-direction:column; align-items:center; gap:4px; flex:none; }}
figcaption {{ font-size:.75rem; color:var(--cap); }}
.ink {{ color:var(--ink); fill:currentColor; }}
.fav {{ fill:var(--fav); }}
.lock {{ display:flex; flex-wrap:wrap; align-items:center; gap:24px; padding:12px 0;
  border-top:1px solid color-mix(in srgb, var(--cap) 30%, transparent); }}
.lock span {{ width:100%; font-size:.875rem; color:var(--cap); }}
.lock img {{ max-width:100%; height:auto; }}
.lock img[height="104"] {{ height:104px; width:auto; }}
.lock img[height="52"] {{ height:52px; width:auto; }}
.lock img[height="28"] {{ height:28px; width:auto; }}
code {{ font-family:"Atkinson Hyperlegible Mono", ui-monospace, Menlo, monospace; font-size:.9em; }}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{symbols}</svg>
<main>
<h1>Shisa: machine-traced vector candidates</h1>
<div class="warn"><b>Candidates, not marks.</b> Everything on this page except the reference rows was produced by
automated tracing (vtracer, potrace) of the 1024 px raster. None of it has been reviewed by a designer, and none of it
replaces a file in <code>marks/mark/</code> or <code>marks/lockup/</code>. Provenance and parameters:
<code>marks/PROVENANCE.md</code>; rebuild with <code>marks/candidates/tools/build.sh</code>.</div>
<p>Each row is shown at 512, 128, 48, 32 and 16 CSS px. The one-colour marks use the ground's text colour
(<code>#faf6fa</code> / <code>#160d15</code>); the one-colour favicon is shown in the colour its
<code>prefers-color-scheme</code> rule would pick for that ground. On a high-DPI screen the small tiles get 2 to 3 device
pixels per CSS pixel, so zoom the browser out, or look at <code>renders/*-16.png</code>, to see a true 16 px tab icon.</p>
{ground("dark")}
{ground("light")}
{"".join(lock)}
</main>
</body>
</html>
"""
(C / "index.html").write_text(html)
print("page: index.html")
