# Marks: provenance and status

## Status

The mark is the shisa mascot. **It exists only as a raster illustration.** No
vector source has been found anywhere in the org or in raskell-io (searched
2026-10-21: every `.svg` under `zentinelproxy/` and `raskell-io/`, both site
repos on GitHub `main`, the `zentinel` repo's `.github/static/`). The only SVG
called `logo.svg` in the org, `zentinel-control-plane/priv/static/images/logo.svg`,
is the Phoenix framework's bird from the project generator, not a Zentinel mark.

So this repo does **not** contain a drawn vector shisa. A hand redraw of the
mark as vector is the open item. `marks/candidates/` holds **machine-traced
candidates** (see [Traced candidates](#traced-candidates-marks-candidates)
below): they are proposals for a designer to review, not marks, and none of
them replaces a file listed here. Until the redraw lands:

| File | What it is | Vector? |
|---|---|---|
| `wordmark/zentinel-wordmark.svg` | "Zentinel" in Unbounded 700, outlined to paths, `fill="currentColor"` (mono) | yes |
| `wordmark/zentinel-wordmark-on-dark.svg` | same, orange-400 `#f68d31` (8.0:1 on the dark ground) | yes |
| `wordmark/zentinel-wordmark-on-light.svg` | same, orange-700 `#9b4804` (5.9:1 on the light ground; orange-400 is only 2.2:1) | yes |
| `mark/zentinel-mark-disc-512.png` | the mascot cropped to its plum disc, corners transparent (derived from the 1024 source by `scripts/marks.ts`) | no |
| `lockup/zentinel-lockup-{dark,light}.svg` | **interim** horizontal lockup: the disc embedded as a 256 px PNG, plus the outlined wordmark | partly |

The wordmark is outlined text, not a font reference, so it needs no font on
the page. `deno task marks` regenerates all of the above.

Blocked on the vector redraw: a mono (one-colour) mark and lockups, an SVG
favicon (`favicon.svg`), a small-size simplified mark (the illustration's
curls and outlines turn to mush below ~32 px, see `source/favicon.png`), and
a stacked lockup. When the redraw lands, put its source in `mark/` and replace
the `<image>` in `scripts/marks.ts`'s lockup template with its paths.

## Sources (`source/`)

Copied byte-for-byte, nothing re-encoded.

| File | Origin | Size | sha256 (first 12) |
|---|---|---|---|
| `zentinel-mascot-1024.png` | `zentinelproxy.io/static/img/zentinel-mascot.png` (identical in `zentinelproxy.io-docs/static/img/` and `zentinel/.github/static/`); in the site's history since `51b69cf` "Rename sentinel → zentinel" (2026-02-17); artist/tool not recorded | 1024×1024 | `fbc021834e6f` |
| `favicon.ico` | `zentinelproxy.io/static/favicon.ico` (16/32/48) | | `72225afce85d` |
| `favicon.png` | `zentinelproxy.io/static/favicon.png` | 32×32 | `63969b7d384d` |
| `icon-192.png` | `zentinelproxy.io/static/icon-192.png` | 192×192 | `26eccf540424` |
| `apple-touch-icon.png` | `zentinelproxy.io/static/apple-touch-icon.png` | 180×180 | `8e87a994eff9` |
| `zentinel-logo-64.avif` | `zentinelproxy.io/static/img/zentinel-logo-64.avif`, added on GitHub `main` in `47188a8` (#32, 2026-10-18); not in the local clone | 64×64 | `b6d966763332` |
| `raskell-brands-zentinel-168.png` | `www.raskell.io/static/brands/zentinel.png` (the project card on raskell.io) | 168×168 | `0d94be87ac69` |

The site files were checked against GitHub `main` by blob SHA on 2026-10-21
(the local clone is behind, but these files are unchanged).

The illustration's own palette is where the brand accents come from: the
orange coat (`#f68d31` in raskell.io's `data/projects/zentinel.toml`) and the
plum disc and ball (`#9b4d8a`).

## Favicon set

Current sources are the rasters above (`favicon.ico`, `favicon.png`,
`icon-192.png`, `apple-touch-icon.png`). They are kept as the source of the
favicon set until a vector mark allows `favicon.svg` plus regenerated PNGs.

## Traced candidates (`marks/candidates/`)

**These are machine-traced candidates pending a designer's review.** They were
produced by automated tracing of `source/zentinel-mascot-1024.png` on
2026-10-21, not drawn. Nothing in `mark/`, `lockup/`, `wordmark/` or the site
favicon set was replaced, and nothing should link to these files as the mark
until someone who can draw has reviewed (or redrawn) them. Open
`marks/candidates/index.html` in a browser to compare them with the raster.

| File | What it is | Bytes |
|---|---|---|
| `zentinel-mark-colour.svg` | full-colour disc, vtracer trace, 13 flat colours, 740-unit viewBox (the disc PNG's frame) | 31,664 |
| `zentinel-mark-mono-line.svg` | one-colour line art of the head, `fill="currentColor"` | 7,774 |
| `zentinel-mark-mono-solid.svg` | one-colour solid head (mane and ears filled, face open, eyes/nose/mouth drawn), `currentColor` | 3,132 |
| `favicon.svg` | the solid head; `#9b4804` (orange-700) by default, `#f68d31` (orange-400) under `prefers-color-scheme: dark` | 3,106 |
| `favicon-colour.svg` | the head in four flat colours (orange-400, cream, outline, nose); no media query | 4,644 |
| `zentinel-lockup-{dark,light}.svg` | the interim lockups' exact geometry and wordmark path, with the traced disc instead of the embedded PNG | 35,212 / 35,214 (interim: 119,469 / 119,470) |
| `renders/*-{16,32,48}.png` | resvg renders for the small-size check (`currentColor` renders black) | |
| `index.html` | comparison page: raster vs each candidate at 512/128/48/32/16 px on both grounds, plus the lockups | |
| `tools/` | the pipeline below | |

### Pipeline and parameters

Rebuild everything with

```bash
TOOLS_VENV=<venv> TOOLS_NODE=<dir> marks/candidates/tools/build.sh
```

where `<venv>` has `vtracer==0.6.15 pillow==11.3.0 numpy==2.0.2 scipy==1.13.1`
(built with Python 3.9.6) and `<dir>/node_modules` has `svgo@3.3.2` and
`@resvg/resvg-js@2.6.2` (Node 26.9.0). `potrace 1.16` must be on `PATH`. The
build is deterministic: two runs give byte-identical outputs.

1. **`tools/prep.py`** (Pillow, NumPy, SciPy). Composites the source on the
   disc colour and crops the same 740 × 740 frame at +142+142 that
   `scripts/marks.ts` uses for the disc PNG. Measured on the source, the disc
   is centred at (512, 503), not (512, 512), with its inner edge at r ≈ 347;
   everything outside r = 344 around that centre is painted with the disc
   colour so the ring can be redrawn as exact circles. Then a 3 × 3 median
   filter and a nearest-colour remap, no dithering, to the 13-colour palette
   in `tools/prep_palette.py` (sampled from the source: outline `#200b22`,
   disc `#492c4f`, orange `#fe8a27`/`#e56c26`/`#fcac2a`, cream
   `#fedaa9`/`#e59c5b`, nose `#885135`, tongue `#ba5760`, white, ball
   `#96749a`/`#664879`/`#d7bdc7`). These are the illustration's own colours,
   not the brand tokens: the coat is `#fe8a27`, close to but not
   `#f68d31`, and the disc is much darker than plum-600 `#9b4d8a`. The mono
   masks come from the same remap: the head is the filled figure above
   y = 425 (the collar line), the features are the 2nd to 4th largest
   components of the outline layer (mouth, left eye + nose, right eye), the
   line art adds a 9 px contour so the cut is closed, and the solid version
   opens the cream areas larger than 800 px.
2. **vtracer** on the remapped disc: `colormode=color hierarchical=stacked
   mode=spline filter_speckle=8 color_precision=8 layer_difference=8
   corner_threshold=60 length_threshold=4.0 max_iterations=10
   splice_threshold=45 path_precision=1`.
3. **potrace** on each mask: `potrace -s -t 24 -a 1.0 -O 0.4`.
4. **`tools/assemble.py`** snaps vtracer's averaged fills back to the
   palette, draws the disc as three concentric circles at (370, 370) (ring
   `#84566a` r 370, line `#281640` r 348, disc `#492c4f` r 346), shifts the
   figure down 9 px so it sits where it does on the source disc, and clips it
   to the disc. Mono and favicon files get `fill="currentColor"` or the
   scheme-aware `<style>`.
5. **svgo 3.3.2** with `tools/svgo.config.cjs`: `preset-default`,
   multipass, `floatPrecision: 1`, keeping title/viewBox/role/comments, with
   `mergePaths` off (it would reorder the stacked colour layers) and
   `inlineStyles` off (it turned the favicon's light rule into a `style`
   attribute that beat the dark-scheme rule).
6. **`tools/lockup.py`** wraps the optimised disc in
   `scale(159.79 / 740)` and copies the wordmark `<path>` and viewBox
   verbatim from `lockup/zentinel-lockup-{dark,light}.svg` (svgo 3.3.2
   crashes in `convertPathData` on that path, so the lockup is not
   re-optimised).
7. **`tools/page.py`** writes `index.html`; resvg renders `renders/`.

### Quality, as traced

- **Full colour**: faithful at 128 px and up. Lost: the soft gradients on the
  coat and ball (now flat bands), the thin light rim along the orange edges,
  and some smoothness (outlines wobble slightly when zoomed). Mush at 32 px
  and below, like the raster.
- **One-colour line**: reads as the shisa at 128 px and up; the curls are the
  recognisable part. At 48 px and below the lines fill in. The left ear's
  outline is open (it is in the source too) and the cut at the collar is a
  straight line.
- **One-colour solid** and **favicon**: the curls are gone, so it reads as a
  smiling, fluffy head rather than specifically a shisa. It holds up at 32
  and 16 px. On a dark ground the open face shows the ground, so the face
  goes dark.
- **Colour favicon**: the most legible at 16 px of the set (cream face, dark
  smile on orange), on dark and light tabs.

Open items for the designer: a drawn mane (curls simplified for small sizes),
a closed left ear, a bust shape instead of a straight cut, and a decision on
whether the mark uses the illustration's colours or the brand tokens.
