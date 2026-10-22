<p align="center">
  <a href="https://zentinelproxy.io">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="marks/lockup/zentinel-lockup-dark.svg">
      <img alt="Zentinel" src="marks/lockup/zentinel-lockup-light.svg" height="52">
    </picture>
  </a>
</p>

<h3 align="center">Zentinel design tokens</h3>

<p align="center">One <code>tokens.json</code> for colour, type, spacing, radius, shadow and motion, compiled for zentinelproxy.io, its docs, the API reference and the agent registry.</p>

<p align="center">
  <a href="https://zentinelproxy.io">Website</a> &middot;
  <a href="https://docs.zentinelproxy.io">Docs</a> &middot;
  <a href="https://github.com/zentinelproxy">All repositories</a>
</p>

## What this is

The single source of truth for Zentinel's look. `build.ts` reads `tokens.json`,
checks every declared text/background pairing against WCAG contrast in both
themes, and writes Sass partials, CSS custom properties and a preview page to
`dist/`. `scripts/sync.ts` then vendors those files into the consumer repos,
so the site, the docs, the API reference and the registry share one palette,
one type scale and one button while staying four separate Zola sites.

It follows the design repo behind cyanea.bio: same
`tokens.json` → `build.ts` → committed copies in each consumer, Deno pinned
through mise. Two differences: the build writes to `dist/` here and a separate
`sync` step copies into the consumers (so a token change is reviewable in this
repo before it lands anywhere), and the build fails on a contrast violation.

## Quickstart

```bash
mise install              # installs the pinned Deno
mise run build            # = deno task build: contrast gate, then dist/
open dist/preview/index.html
```

| Task | What it does |
|---|---|
| `deno task build` | gate contrast, write `dist/` (CSS, Sass, resolved JSON, preview) |
| `deno task check` | gate contrast only, write nothing (for CI) |
| `deno task sync` | copy `dist/` + `fonts/` into the four consumers checked out next to this repo |
| `deno task sync --check` | report consumer copies that are stale, exit 1 if any |
| `deno task sync --check --root <dir>` | the same, with the consumers under `<dir>` (or `DESIGN_CONSUMER_ROOT`) instead of `..` |
| `deno task sync --check --strict` | also fail when a consumer is not checked out (what CI runs) |
| `deno task marks` | regenerate the outlined wordmark and the interim raster lockups in `marks/lockup/interim/` (network + ImageMagick) |
| `deno task ramps` | print the colour ramps derived from the brand accents |

## Structure

```
design/
├── tokens.json          # the tokens (edit this)
├── build.ts             # compiler + contrast gate + preview
├── lib/color.ts         # WCAG contrast, OKLCH conversions
├── scripts/
│   ├── sync.ts          # vendor dist/ into consumers, or --check them for drift
│   ├── marks.ts         # outline the wordmark, build lockups
│   └── ramps.ts         # derive ramps from #f68d31 / #9b4d8a
├── components/
│   └── controls.css     # control styles, appended to frame.css by the build
├── fonts/               # WOFF2 + OFL licence files (see fonts/README.md)
├── marks/               # sources, wordmark, mark, lockups (see marks/PROVENANCE.md)
├── .github/workflows/
│   ├── ci.yml           # contrast gate + dist/ is what tokens.json builds to
│   └── drift.yml        # the four consumers' main still match dist/
├── dist/                # GENERATED, committed
│   ├── css/{tokens,fonts,frame,bridge}.css
│   ├── scss/_{tokens,fonts,frame}.scss
│   ├── tokens.resolved.json, contrast.json
│   └── preview/index.html
├── deno.json
└── mise.toml
```

## How consumers use it

Each consumer **commits its vendored copy**, the same mechanism cyanea uses
(no submodule, no package). A consumer therefore
builds on its own, and Cloudflare Pages never needs this repo.

Check the consumers out next to this repo (each under its repo name), then
`deno task build && deno task sync`:

| Consumer | Files it receives | How it loads them |
|---|---|---|
| `zentinelproxy.io` (Zola + Sass) | `sass/_tokens.scss`, `sass/_fonts.scss`, `sass/_frame.scss`, `static/fonts/*` | `@import 'tokens'; @import 'fonts'; @import 'frame';` at the top of `sass/style.scss`, then use `var(--z-*)` |
| `registry.zentinelproxy.io` (Zola + Sass) | the same as `zentinelproxy.io` | the same |
| `zentinelproxy.io-docs` (Zola + tanuki submodule) | `static/css/zentinel-{fonts,tokens,bridge,frame}.css`, `static/fonts/*` | `<link>` them in that order from the docs' own template override, **after** the theme stylesheet. The docs restyle lives in the docs repo as overrides; tanuki is not edited |
| `api.zentinelproxy.io` (Zola, plain CSS) | `static/css/{tokens,fonts,frame}.css`, `static/fonts/*` | `<link>` from its own templates |

A new consumer is one entry in `CONSUMERS` in `scripts/sync.ts` plus one
checkout step in `.github/workflows/drift.yml`.

### The tanuki bridge

`bridge.css` lets any site on the tanuki theme follow the tokens without
forking the theme. It is custom properties on `:root` only, no selectors, and
it maps:

- tanuki's semantic names: `--color-bg`, `--color-bg-surface`,
  `--color-text-muted`, `--color-accent`, `--color-border-strong`, … and the
  site's legacy `--color-primary` / `--color-bg-subtle`;
- the Catppuccin palette tanuki's components read directly (`--ctp-base`,
  `--ctp-mantle`, `--ctp-surface0`, `--ctp-mauve`, `--ctp-blue`, … all 26);
- `--radius-sm/md/lg/xl` (tanuki's lg/xl take our md/lg), `--shadow-sm/md/lg/xl`,
  and `--shadow-glow` (off);
- `--font-sans` / `--font-mono`, and tanuki's comma-form `--color-bg-rgb` /
  `--color-accent-rgb` per theme.

tanuki's `[data-theme]` attribute on `<html>` drives both. What a variable
cannot reach stays a selector override in the consumer: tanuki's `h1`–`h6`
rule sets `color: var(--color-text)` rather than `--color-heading`, and a few
tanuki rules hard-code Catppuccin hexes (`pre`, the code header bar).

### Channel variables

Every `--z-*-rgb` is **space-separated** `R G B`, used as
`rgb(var(--z-bg-rgb) / 0.8)`: `--z-shadow-rgb` and the derived
`--z-bg-rgb`, `--z-surface-rgb`, `--z-surface-raised-rgb`, `--z-text-rgb`,
`--z-accent-rgb`, `--z-accent-2-rgb`, set per theme in `tokens.css`. The only
comma-separated triplets are tanuki's own `--color-bg-rgb` and
`--color-accent-rgb` in `bridge.css`, kept in that form because tanuki writes
`rgba(var(--color-bg-rgb), 0.8)`; new code should not use them.

### Gradients

`--z-gradient-brand` (orange-400 → plum-600) is decorative: bars, rules,
fills. It fails contrast for text at one end in each theme. For gradient text
use `--z-gradient-brand-text` (`accent-text` → `accent-2-text`, per theme)
with `background-clip: text`. The build gates both stops and the colour at
25/50/75 % against `bg`, `surface` and `surface-raised`.

Never edit a vendored file in a consumer: the next sync overwrites it, and
the drift check reports it.

## Drift

`.github/workflows/drift.yml` runs on every push to main, on pull requests
and daily. It checks out the four consumers' `main` next to this repo and runs
`deno task sync --check --strict --root "$GITHUB_WORKSPACE"`. The job summary
lists each consumer as up to date or stale, with the files that differ. On a
pull request that changes tokens, drift is expected and the step only reports;
on main and on the daily run it fails.

When it reports a consumer as stale:

1. Check out that consumer next to this repo (or pass `--root`).
2. Here, on an up-to-date main: `deno task build && deno task sync`.
3. In the consumer: review the diff, build it, commit the vendored files
   (and nothing else) in one commit, and open a PR there.
4. If the stale file was edited by hand in the consumer, move that change into
   `tokens.json` (or `components/`) here first; the sync reverts it.

Each consumer can carry the same check from its side: a job that checks out
this repo at `main` and runs `deno task sync --check --root ..` against its
own checkout (only that consumer is present, so the others are skipped). No
secret is needed; every repo here is public.

## Changing a token

1. Edit `tokens.json`. Semantic roles and component tokens reference
   primitives as `{orange.400}`; never put a raw hex in `semantic`.
2. `deno task build`. If a pairing drops below its minimum the build stops
   and names it, e.g. `[dark] on-accent-2 #faf6fa on accent-2-hover #b968a7: 3.5:1 < 4.5:1`.
   Pick another step; do not lower the level.
3. Open `dist/preview/index.html` and look at both themes.
4. Commit here (`tokens.json` and `dist/` together), then `deno task sync`
   and commit the copies in each consumer.

Adding a role: add it to **both** `semantic.dark` and `semantic.light` (the
build refuses a mismatch) and, if it is ever text or a UI boundary, to a
`contrast` rule. Retuning a ramp: change the curve in `scripts/ramps.ts`,
`deno task ramps`, paste over `color`, rebuild. Brand hexes stay pinned
(`#f68d31` = `orange.400`, `#9b4d8a` = `plum.600`).

## Token structure

- **color**: ramps 50–950 for `orange` (shisa), `plum`, `neutral`
  (plum-tinted greys, plus `0` white and an `850` raised surface), and
  `green`/`amber`/`red`/`blue` for status. Derived in OKLCH from the two
  accents; no Catppuccin values.
- **semantic.dark / semantic.light**: `bg`, `surface`, `surface-raised`,
  `border` (decorative), `border-strong` (UI, ≥3:1), `text`, `heading`,
  `muted`, `accent` (fill) / `accent-hover` / `on-accent` / `accent-text`,
  the same four for `accent-2`, `link`/`link-hover`, `focus`,
  `success`/`warn`/`danger`/`info`, `code-bg`/`code-fg`/`code-accent`,
  `selection-bg`/`selection-fg`, `button-edge`/`button-2-edge`, and
  `shadow-rgb` (plus the derived `*-rgb` channels, see above). Dark is the default ground; `[data-theme="light"]` or the OS
  preference switches.
- **contrast**: the pairings the build checks. 72 per theme today (with the
  text-gradient samples), all passing (lowest text pairing 5.14:1 dark,
  4.76:1 light).
- **font**: Unbounded (display), Atkinson Hyperlegible Next (text),
  Atkinson Hyperlegible Mono (code), all OFL 1.1. **fontFace** lists the
  WOFF2 files.
- **fontSize** (1.25 ratio), **fontWeight**, **lineHeight**, **letterSpacing**,
  **space** (4 px steps), **layout**, **radius**, **shadow** (tinted per theme).
- **button**: the family's raised "physical" CTA (`.z-btn` in `frame.css`):
  a hard 4 px edge under the face, lifts to 6 px on hover, presses to 1 px.
- **control**: heights (sm/md/lg), the 44 px touch target, radius, border,
  check and switch sizes for the controls in `components/controls.css`
  (appended to `frame.css`): `.z-input`, `.z-textarea`, `.z-select`,
  `.z-check` (checkbox/radio), `.z-switch`, `.z-choice` (radio cards),
  `.z-segmented`, `.z-tabs`, `.z-copy`, `.z-menu`, `.z-tooltip`, `.z-kbd`, and
  the button sizes and states `.z-btn--sm/--lg/--ghost/--icon`, `:disabled`,
  `aria-busy="true"` (loading). All class-scoped, so they never restyle a
  consumer theme by element.
- **gradient** (decorative) and **gradientText** (stops are roles, gated
  for text).
- **motion** + **reducedMotion**: durations and easings; under
  `prefers-reduced-motion: reduce` durations go to 0 and `--z-lift` to 0, so
  the button keeps its colour feedback and stops moving.

Custom properties are prefixed `--z-` (`--z-bg`, `--z-orange-400`,
`--z-size-xl`); Sass variables `$z-` (`$z-orange-400`, `$z-dark-bg`, maps
`$z-theme-dark`/`$z-theme-light`, `@include z-theme(light)`).

## Marks

The mark is the shisa mascot, drawn as a raster illustration. The wordmark is
vector (outlined Unbounded 700). The lockups in `marks/lockup/` use a
machine-traced vector of the disc, which stands in until a designer redraws the
mascot; the earlier raster-disc lockups are kept in `marks/lockup/interim/`.
Details and provenance: [`marks/PROVENANCE.md`](marks/PROVENANCE.md).

## License

The code and tokens are MIT (see [`LICENSE`](LICENSE)), like the site. The
fonts are under the SIL Open Font License 1.1; each family's license file sits
next to it in `fonts/`. The shisa, the wordmark and the lockups are Zentinel's
marks: use them to refer to Zentinel, not as the mark of something else.

---

<p align="center">
  <sub>Part of <a href="https://zentinelproxy.io">Zentinel</a>, the security-first reverse proxy. The shisa guards the gate.</sub>
</p>
