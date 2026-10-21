<p align="center">
  <a href="https://zentinelproxy.io">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/zentinelproxy/design/main/marks/lockup/zentinel-lockup-dark.svg">
      <img alt="Zentinel" src="https://raw.githubusercontent.com/zentinelproxy/design/main/marks/lockup/zentinel-lockup-light.svg" height="52">
    </picture>
  </a>
</p>

<h3 align="center">{Name} agent</h3>

<p align="center">{One sentence: what it inspects or enforces, and where in the request it runs.}</p>

<p align="center">
  [![CI](https://github.com/zentinelproxy/{REPO}/actions/workflows/{WORKFLOW}.yml/badge.svg)](https://github.com/zentinelproxy/{REPO}/actions/workflows/{WORKFLOW}.yml)
  ![License](https://img.shields.io/badge/license-{SPDX}-9b4d8a?style=flat&labelColor=1f161e)
  ![Agent protocol](https://img.shields.io/badge/agent%20protocol-v2-f68d31?style=flat&labelColor=1f161e)
</p>

<p align="center">
  <a href="https://registry.zentinelproxy.io/{name}/">Registry</a> &middot;
  <a href="https://docs.zentinelproxy.io">Docs</a> &middot;
  <a href="https://github.com/zentinelproxy">All repositories</a>
</p>

{Two to four sentences: the problem, for whom, how it decides, what happens on failure (`failure-mode`).}

## Quick start

```bash
zentinel bundle install {name}   # only if the agent is in the bundle; otherwise see Install
```

```kdl
{The smallest config that wires this agent into a route: an `agents` block
and a route that uses it. It must pass `zentinel test -c <file>`; take the
syntax from https://docs.zentinelproxy.io/configuration/agents/, not memory.}
```

## Install

{Every supported way, recommended first. Only commands verified to work.}

## Configuration

| Option | Default | Meaning |
|---|---|---|
| `{option}` | `{default}` | {what it does} |

Full reference: <https://registry.zentinelproxy.io/{name}/>

## How it works

{Optional. Short.}

## Development

```bash
cargo test
cargo clippy --all-targets -- -D warnings
```

## Related

- [Registry page](https://registry.zentinelproxy.io/{name}/)
- [Agent protocol v2](https://docs.zentinelproxy.io/agents/v2/)
- [Zentinel](https://github.com/zentinelproxy/zentinel)

## License

{SPDX}, see [`LICENSE`](LICENSE).

---

<p align="center">
  <sub>Part of <a href="https://zentinelproxy.io">Zentinel</a>, the security-first reverse proxy. The shisa guards the gate.</sub>
</p>
