# Fonts

Self-hosted WOFF2, so pages render without third-party font requests. All
three families are licensed under the **SIL Open Font License 1.1**; the
licence text for each sits next to its files and must ship with them.

| Role | Family | Files | Axes | Licence |
|---|---|---|---|---|
| Display (headings, wordmark) | [Unbounded](https://github.com/googlefonts/unbounded) | `unbounded-latin{,-ext}-wght-normal.woff2` | wght 200–900 | OFL 1.1, `Unbounded-OFL.txt` |
| Text (body, UI) | [Atkinson Hyperlegible Next](https://github.com/googlefonts/atkinson-hyperlegible-next) (Braille Institute) | `atkinson-hyperlegible-next-latin{,-ext}-wght-{normal,italic}.woff2` | wght 200–800, ital | OFL 1.1, `AtkinsonHyperlegibleNext-OFL.txt` |
| Mono (code, config) | [Atkinson Hyperlegible Mono](https://github.com/googlefonts/atkinson-hyperlegible-next-mono) (Braille Institute) | `atkinson-hyperlegible-mono-latin{,-ext}-wght-{normal,italic}.woff2` | wght 200–800, ital | OFL 1.1, `AtkinsonHyperlegibleMono-OFL.txt` |

Source: the Latin and Latin Extended subsets of the Fontsource variable
builds, version 5.3.0 (`@fontsource-variable/unbounded`,
`@fontsource-variable/atkinson-hyperlegible-next`,
`@fontsource-variable/atkinson-hyperlegible-mono` on npm), copied unmodified.
The licence files are the `LICENSE` from each package. The unicode ranges in
`tokens.json` are Fontsource's.

The wordmark in `marks/` is outlined from the static Unbounded 700 WOFF
(`@fontsource/unbounded@5.3.0`), fetched at `deno task marks` time and not
stored here.

## Why these

- Distinct from the family: raskell.io uses Seijaku Sans/Mono, cyanea.bio
  Bricolage Grotesque + Inter + JetBrains Mono, archipelag.io Satoshi,
  arcanist.sh Funnel Display + Geist. zentinelproxy.io currently uses Geist +
  Geist Mono, which this replaces.
- Unbounded is wide and rounded at the terminals: it reads as solid and
  friendly, which suits a guardian mascot, and holds up as a wordmark.
- Atkinson Hyperlegible was drawn for low-vision readers: it disambiguates
  `I l 1 |` and `O 0`, which matters for docs full of config keys, IPs and
  hashes. The Mono cut keeps the same letterforms in code blocks.
