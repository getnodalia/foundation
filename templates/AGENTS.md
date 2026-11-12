# <App>: instructions for agents

<!-- Nodalia template: https://github.com/getnodalia/foundation/blob/main/standards/agents.md
     General rules (engineering, CI, security, release, NDL) live in getnodalia/foundation and are
     not repeated here. This file holds only what is particular to this repository. -->

Engineering rules for every Nodalia repository: [getnodalia/foundation](https://github.com/getnodalia/foundation)
([engineering](https://github.com/getnodalia/foundation/blob/main/standards/engineering.md),
[CI](https://github.com/getnodalia/foundation/blob/main/standards/ci.md),
[security](https://github.com/getnodalia/foundation/blob/main/standards/security.md),
[release](https://github.com/getnodalia/foundation/blob/main/standards/release.md),
[NDL](https://github.com/getnodalia/foundation/blob/main/standards/ndl.md)).

## What this is

<One paragraph: what the app does, for whom, platforms and editions.> App ID `dev.danielmiguelt.<App>`.
Licence: <SPDX>. <If inherited: origin credited in NOTICE.>

## Architecture

| Path | Responsibility |
|---|---|
| `crates/<x>` | ... |

Dependency direction: ... A new feature of kind X goes in ...

## Build and test

```bash
<gate command>          # what CI runs; run before every commit
<fast loop>
<run the app>
```

Tests that need extra inputs (fonts, corpora, GPU) and how they skip without them: ...

## Rules

- <Rule> (enforced by <check>).

## NDL

Package and pin: ... Integrated: ... Missing: ... (details in NODALIA_MIGRATION.md).

## Release

Workflow: ... Artifacts: ... Maintainer steps: push tag `vX.Y.Z`, review the draft, publish.

## Pull requests

A change is ready when: the gate passes, new behaviour has a test that fails without it, UI changes
come with a screenshot taken from the running app, and docs that describe the behaviour are updated.

## Known traps

- ...
