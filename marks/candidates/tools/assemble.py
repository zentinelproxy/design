"""Wrap the raw traces into the candidate SVGs (pre-svgo).

usage: python assemble.py <workdir> <repo-root>

Reads <workdir>/{colour-raw.svg, head-line-raw.svg, head-solid-raw.svg} and the
interim lockups in marks/lockup/, writes <workdir>/out/*.svg (svgo runs after).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from prep_palette import PALETTE, RING  # noqa: E402

WORK, ROOT = Path(sys.argv[1]), Path(sys.argv[2])
OUT = WORK / "out"
OUT.mkdir(exist_ok=True)

CAND = "MACHINE-TRACED CANDIDATE, pending a designer's review. Not a shipped mark. See marks/PROVENANCE.md."

# Disc geometry in the 740-px frame (the frame of marks/mark/zentinel-mark-disc-512.png).
RING_LINE = "#281640"
DISC = PALETTE["disc"]


def hexrgb(h):
    return tuple(int(h[i : i + 2], 16) for i in (1, 3, 5))


pal = [(n, hexrgb(h), h) for n, h in PALETTE.items()]


def snap(h):
    r = hexrgb(h)
    return min(pal, key=lambda p: sum((a - b) ** 2 for a, b in zip(p[1], r)))[2]


# ---- full-colour disc ---------------------------------------------------------
raw = (WORK / "colour-raw.svg").read_text()
paths = []
for d, fill, tx, ty in re.findall(
    r'<path d="([^"]+)" fill="(#[0-9A-Fa-f]{6})" transform="translate\(([-\d.]+),([-\d.]+)\)"/>', raw
):
    t = "" if (float(tx), float(ty)) == (0, 0) else f' transform="translate({tx} {ty})"'
    paths.append(f'<path fill="{snap(fill)}"{t} d="{d.strip()}"/>')

# The figure is traced in source position; the disc centre in the source is
# (370, 361) in this frame, so shift the figure down 9 px to centre it in a
# geometric disc at (370, 370).
disc_body = (
    f'<defs><clipPath id="zs-disc"><circle cx="370" cy="361" r="346"/></clipPath></defs>\n'
    f'<circle cx="370" cy="370" r="370" fill="{RING}"/>\n'
    f'<circle cx="370" cy="370" r="348" fill="{RING_LINE}"/>\n'
    f'<circle cx="370" cy="370" r="346" fill="{DISC}"/>\n'
    f'<g clip-path="url(#zs-disc)" transform="translate(0 9)">\n' + "\n".join(paths) + "\n</g>"
)
colour = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 740" role="img" aria-label="Zentinel shisa">\n'
    f"<!-- {CAND} Full-colour vtracer trace of marks/source/zentinel-mascot-1024.png, disc frame. -->\n"
    "<title>Zentinel shisa (traced candidate)</title>\n" + disc_body + "\n</svg>\n"
)
(OUT / "zentinel-mark-colour.svg").write_text(colour)


# ---- one-colour head ------------------------------------------------------------
def potrace_body(name):
    s = (WORK / f"{name}-raw.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    g = re.search(r'<g transform="([^"]+)"', s).group(1)
    ds = re.findall(r'<path d="([^"]+)"', s)
    d = " ".join(" ".join(x.split()) for x in ds)
    return vb, g, d


def mono(name, label, extra=""):
    vb, g, d = potrace_body(name)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Zentinel">\n'
        f"<!-- {CAND} One-colour {label}: potrace of a mask derived from the traced palette (fill=currentColor). -->\n"
        f"<title>Zentinel (traced candidate)</title>\n{extra}"
        f'<path fill="currentColor" transform="{g}" d="{d}"/>\n</svg>\n'
    )


(OUT / "zentinel-mark-mono-line.svg").write_text(mono("head-line", "line art of the head"))
(OUT / "zentinel-mark-mono-solid.svg").write_text(mono("head-solid", "solid head, face open"))

# ---- favicon: solid head, scheme-aware ----------------------------------------
vb, g, d = potrace_body("head-solid")
fav = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">\n'
    f"<!-- {CAND} Favicon: the solid one-colour head. orange-700 on light tabs, orange-400 on dark tabs. -->\n"
    "<style>path{fill:#9b4804}@media (prefers-color-scheme:dark){path{fill:#f68d31}}</style>\n"
    f'<path transform="{g}" d="{d}"/>\n</svg>\n'
)
(OUT / "favicon.svg").write_text(fav)

# Colour favicon: orange head, cream face, dark features; no media query needed.
layers = []
for name, fill in (("head-fill", "#f68d31"), ("head-face", PALETTE["cream"]), ("head-feat", PALETTE["outline"]), ("head-nose", PALETTE["nose"])):
    _, gl, dl = potrace_body(name)
    layers.append(f'<path fill="{fill}" transform="{gl}" d="{dl}"/>')
favc = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">\n'
    f"<!-- {CAND} Favicon variant: the head in four flat colours (orange-400, cream, outline, nose); same on any tab colour. -->\n"
    + "\n".join(layers) + "\n</svg>\n"
)
(OUT / "favicon-colour.svg").write_text(favc)

print("assemble: wrote", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
