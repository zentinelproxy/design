# README standard

Every README in the zentinelproxy organization follows this format, so a
visitor who lands on any repository sees the same frame, the same voice and
the same order of information as on zentinelproxy.io. The org profile
(`zentinelproxy/.github`, `profile/README.md`) uses the same frame.

Copy the matching template from [`templates/`](templates/) and fill it in.

## Frame

### Header

```html
<p align="center">
  <a href="https://zentinelproxy.io">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/zentinelproxy/design/main/marks/lockup/zentinel-lockup-dark.svg">
      <img alt="Zentinel" src="https://raw.githubusercontent.com/zentinelproxy/design/main/marks/lockup/zentinel-lockup-light.svg" height="52">
    </picture>
  </a>
</p>

<h3 align="center">{Name}</h3>

<p align="center">{One sentence: what it is and who it is for.}</p>

<p align="center">{badges}</p>

<p align="center">
  <a href="{primary link}">{label}</a> &middot;
  <a href="https://docs.zentinelproxy.io">Docs</a> &middot;
  <a href="https://github.com/zentinelproxy">All repositories</a>
</p>
```

- The lockup is always loaded from this repository's `main` by absolute URL,
  never from zentinelproxy.io (site assets move; the 2026-10 restyle removed
  the old `logo-*.svg` and broke the org profile) and never copied into the
  repository.
- `{Name}`: the human name, e.g. "WAF agent", "Go agent SDK", "Zentinel
  control plane". The core repository uses the tagline instead.
- Link row: the most useful page first. For an agent, its registry page
  (`https://registry.zentinelproxy.io/<name>/`); for an SDK, the agent protocol docs (`https://docs.zentinelproxy.io/agents/v2/`);
  for a site, the live URL.

### Badges

At most four, in this order, all `style=flat`:

Write them as HTML, one per line inside the centered `<p>`. Markdown image
syntax is not parsed inside an HTML block, so `![..](..)` there shows up on
GitHub as literal text.

| Badge | HTML |
|---|---|
| CI (only if the repository has a workflow that runs on the default branch) | `<a href="https://github.com/zentinelproxy/<repo>/actions/workflows/<file>.yml"><img alt="CI" src="https://github.com/zentinelproxy/<repo>/actions/workflows/<file>.yml/badge.svg"></a>` |
| License (the SPDX id in `LICENSE`, not in a manifest; no badge if there is no `LICENSE` file) | `<img alt="License: <SPDX>" src="https://img.shields.io/badge/license-<SPDX>-9b4d8a?style=flat&labelColor=1f161e">` |
| Language / toolchain minimum, only if it is enforced somewhere (MSRV in `Cargo.toml`, `go` line in `go.mod`, `engines`, `requires-python`) | `<img alt="Rust 1.85+" src="https://img.shields.io/badge/rust-1.85%2B-f68d31?style=flat&labelColor=1f161e&logo=rust&logoColor=white">` |
| Agent protocol, agents and SDKs only | `<img alt="Agent protocol v2" src="https://img.shields.io/badge/agent%20protocol-v2-f68d31?style=flat&labelColor=1f161e">` |

Colors: `f68d31` (shisa orange) or `9b4d8a` (plum) on label `1f161e`. No
Catppuccin hexes (`c6a0f6`, `f5a97f`, ...), no `for-the-badge`, no badges
for things that are not checked (stars, "PRs welcome", "made with").

### Footer

```html
---

<p align="center">
  <sub>Part of <a href="https://zentinelproxy.io">Zentinel</a>, the security-first reverse proxy. The shisa guards the gate.</sub>
</p>
```

## Order of sections

Use only the sections that have something true to say. Headings are sentence
case (`## Quick start`, not `## Quick Start`).

1. **What it does**: two to four sentences, no heading needed under the
   header. What problem, for whom, and the one thing that makes it different.
2. **Quick start**: the shortest path to seeing it work, copy-pasteable.
3. **Install**: every supported way, the recommended one first. Only commands
   that work today (see "Claims" below).
4. **Configuration**: a minimal, valid KDL block plus a table of options
   (`Option | Default | Meaning`). Link the full reference in the docs rather
   than duplicating it.
5. **How it works**: optional, short; a diagram only if it shows the real
   mechanism.
6. **Development**: build, test and lint commands (prefer the repository's
   `mise` tasks if it has them), and the minimum toolchain.
7. **Related**: links to the docs page, the registry page, sibling
   repositories.
8. **License**: one line naming the licence and linking `LICENSE`.

## Voice

The site's voice: plain, specific, checkable.

- Say what it does and how it is bounded. No "next-generation",
  "enterprise-grade", "blazing fast", "cutting-edge", "seamless", no
  emoji in headings or lists.
- Numbers only when they come from a measurement in the repository or on
  zentinelproxy.io/benchmarks, and say where they come from.
- American English (`license`, `behavior`, `color`), matching the code.
- "Zentinel" for the project, `zentinel` for the binary, "agent" for an
  external processor, "agent protocol v2" for the protocol.

## Claims

A README is checked against the code it describes, like the site:

- Every command must work today. Agent crates are **not on crates.io**, so
  `cargo install zentinel-agent-<x>` is wrong; use `zentinel bundle install
  <x>` if the agent is in the bundle (`api.zentinelproxy.io/v1/bundle/`),
  otherwise `cargo install --git https://github.com/zentinelproxy/<repo>`
  (only if it builds that way) or the release binaries. The Python SDK is
  not on PyPI.
- Every feature listed must exist in the code, and every config key must be
  one the code reads (KDL silently drops unknown keys, so a wrong key in a
  README is a silent no-op for whoever copies it). Mark anything partial or
  experimental as such, or remove it.
- Links must resolve (check each one; there are no per-agent pages on the docs
  site, an agent's reference is its registry page). The docs live at `https://docs.zentinelproxy.io/`
  (`zentinelproxy.io/docs/` is only a redirect); the registry at
  `https://registry.zentinelproxy.io/<name>/`.
- Version numbers and minimum toolchains come from the manifest, not memory.
