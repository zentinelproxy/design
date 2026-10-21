# Marks: provenance and status

## Status

The mark is the shisa mascot. **It exists only as a raster illustration.** No
vector source has been found anywhere in the org or in raskell-io (searched
2026-10-21: every `.svg` under `zentinelproxy/` and `raskell-io/`, both site
repos on GitHub `main`, the `zentinel` repo's `.github/static/`). The only SVG
called `logo.svg` in the org, `zentinel-control-plane/priv/static/images/logo.svg`,
is the Phoenix framework's bird from the project generator, not a Zentinel mark.

So this repo does **not** contain a vector shisa, and nothing here traces or
auto-vectorises the PNG to fake one. A hand redraw of the mark as vector is
the open item. Until then:

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
