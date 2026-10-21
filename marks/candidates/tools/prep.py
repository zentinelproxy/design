"""Raster pre-processing for the machine-traced shisa candidates.

usage: python prep.py <source-1024.png> <workdir>

Writes into <workdir>:
  colour-q.png     the disc crop (740 px, same frame as marks/mark/zentinel-mark-disc-512.png),
                   median-filtered and remapped to a fixed 13-colour palette, ring painted out
  head-line.pbm    one-colour line art of the head (outline layer + closing contour)
  head-solid.pbm   one-colour solid head: mane/ears filled, face open, eyes/nose/mouth drawn
  head-{fill,face,feat,nose}.pbm  the layers of the colour favicon
  head-box.txt     "x y size" of the square head crop in 740-px disc coordinates
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

sys.path.insert(0, str(Path(__file__).parent))
from prep_palette import PALETTE  # noqa: E402

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

# Frame: the same 740x740 crop at +142+142 that scripts/marks.ts uses for the disc.
FX = FY = 142
N = 740
# Measured on the source: the plum disc's inner edge (the thin dark line inside
# the mauve ring) is centred at (512, 503) with r ~ 347-350, not at (512, 512).
DISC_C = (512 - FX, 503 - FY)
DISC_R_INNER = 344  # everything outside is painted with the disc colour; ring is redrawn as circles
HEAD_CUT = 425  # y (disc coords) below which the head mark is cut off (collar line)



def rgb(h):
    return np.array([int(h[i : i + 2], 16) for i in (1, 3, 5)])


src = Image.open(SRC).convert("RGBA")
bg = Image.new("RGBA", src.size, PALETTE["disc"])
flat = Image.alpha_composite(bg, src).convert("RGB").crop((FX, FY, FX + N, FY + N))
a = np.array(flat).astype(int)
yy, xx = np.mgrid[:N, :N]
inside = (xx - DISC_C[0]) ** 2 + (yy - DISC_C[1]) ** 2 < DISC_R_INNER**2
a[~inside] = rgb(PALETTE["disc"])
img = Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.MedianFilter(3))

# Nearest-palette remap, no dithering.
pal = np.stack([rgb(h) for h in PALETTE.values()])
px = np.array(img).astype(int)
idx = ((px[:, :, None, :] - pal[None, None]) ** 2).sum(-1).argmin(-1)
q = pal[idx].astype(np.uint8)
Image.fromarray(q).save(OUT / "colour-q.png")

names = list(PALETTE)
is_ = lambda n: idx == names.index(n)  # noqa: E731

# ---- one-colour masks -------------------------------------------------------
dark = is_("outline") & inside
fig = (~is_("disc")) & inside
fig = nd.binary_opening(fig, iterations=1)
lab, n = nd.label(fig)
fig = lab == (np.argmax(nd.sum(fig, lab, range(1, n + 1))) + 1)
fig = nd.binary_fill_holes(fig)
head = fig & (yy < HEAD_CUT)
lab, n = nd.label(head)
head = lab == (np.argmax(nd.sum(head, lab, range(1, n + 1))) + 1)

# Face features = the 2nd..4th largest components of the outline layer
# (mouth, left eye + nose, right eye); the largest is the body outline network.
lab, n = nd.label(dark)
sz = nd.sum(dark, lab, range(1, n + 1))
feat = np.zeros_like(dark)
for i in np.argsort(-sz)[1:4]:
    feat |= lab == (i + 1)

# Line art: outline layer inside the head, plus a 9 px contour so the cut is closed.
contour = head & ~nd.binary_erosion(head, iterations=9)
line = (dark & head) | contour

# Solid: head filled, large cream areas (face, inner ears) opened, features re-drawn.
cream = is_("cream") & head
lab, n = nd.label(cream)
sz = nd.sum(cream, lab, range(1, n + 1))
open_ = np.zeros_like(cream)
for i in np.argsort(-sz):
    if sz[i] < 800:
        break
    open_ |= lab == (i + 1)
open_ = nd.binary_closing(nd.binary_fill_holes(open_), iterations=2)
solid = head & ~(open_ & ~feat)

# Square crop around the head, 3% padding.
ys, xs = np.nonzero(head)
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
size = int(max(x1 - x0, y1 - y0) * 1.06)
cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
bx, by = cx - size // 2, cy - size // 2


def save(m, name):
    pad = np.zeros((N + 2 * size, N + 2 * size), bool)
    pad[size : size + N, size : size + N] = m
    crop = pad[by + size : by + 2 * size, bx + size : bx + 2 * size]
    Image.fromarray(np.where(crop, 0, 255).astype(np.uint8)).convert("1").save(OUT / name)


save(line, "head-line.pbm")
save(solid, "head-solid.pbm")
# Layers for the colour favicon: orange head, cream face, dark features.
save(head, "head-fill.pbm")
save(open_ & ~feat, "head-face.pbm")
save(feat & head, "head-feat.pbm")
nose = nd.binary_closing(is_("nose") & head, iterations=2)
lab, n = nd.label(nose)
nose = lab == (np.argmax(nd.sum(nose, lab, range(1, n + 1))) + 1)  # the nose, not ear shading
save(nose, "head-nose.pbm")
(OUT / "head-box.txt").write_text(f"{bx} {by} {size}\n")
print(f"prep: colour-q.png, head box x={bx} y={by} size={size}")
