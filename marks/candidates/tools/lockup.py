"""Vector lockup candidates: the interim lockups' geometry with the optimised
traced disc (marks/candidates/zentinel-mark-colour.svg) in place of the PNG.

usage: python lockup.py <repo-root>

The wordmark <path> is copied verbatim from marks/lockup/zentinel-lockup-*.svg
(svgo 3.3.2 crashes on it), so only the disc is re-optimised.
"""

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
CAND = ROOT / "marks/candidates"
disc = (CAND / "zentinel-mark-colour.svg").read_text()
body = re.search(r"</title>(.*)</svg>", disc, re.S).group(1).strip()

for theme in ("dark", "light"):
    src = (ROOT / f"marks/lockup/zentinel-lockup-{theme}.svg").read_text()
    size = float(re.search(r'<image width="([\d.]+)"', src).group(1))
    word = re.search(r"<path transform=[^>]+/>", src).group(0)
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    out = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Zentinel">\n'
        f"<!-- MACHINE-TRACED CANDIDATE, pending a designer's review. Not a shipped mark. See marks/PROVENANCE.md. "
        f"Lockup on {theme}: geometry of marks/lockup/zentinel-lockup-{theme}.svg with the traced vector disc "
        f"in place of the embedded PNG. Wordmark is outlined Unbounded 700 (OFL 1.1). -->\n"
        "<title>Zentinel</title>\n"
        f'<g transform="scale({size / 740:.6f})">{body}</g>\n{word}\n</svg>\n'
    )
    (CAND / f"zentinel-lockup-{theme}.svg").write_text(out)
    print(f"lockup: zentinel-lockup-{theme}.svg")
