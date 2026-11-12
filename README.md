# Nodalia Foundation

The engineering base of every Nodalia repository: the standards, the reusable GitHub Actions
workflows, the templates and the ecosystem status. `getnodalia/.github` keeps the organization
profile; this repository holds everything an app needs to build, test and release the Nodalia way.

## Contents

| Path | What |
|---|---|
| [`standards/engineering.md`](standards/engineering.md) | Code, tests, reviews, branch protection, by stack |
| [`standards/ci.md`](standards/ci.md) | The three CI layers, the zero-cost rule, the shared workflows and how to call them |
| [`standards/security.md`](standards/security.md) | Reporting, secrets, supply chain, repository settings |
| [`standards/dependencies.md`](standards/dependencies.md) | Licence allowlist, inherited code, the code vendored here |
| [`standards/release.md`](standards/release.md) | Versioning and the release pipeline per platform |
| [`standards/agents.md`](standards/agents.md) | What every `AGENTS.md` contains, and the rules every agent follows |
| [`standards/ndl.md`](standards/ndl.md) | How apps consume the Nodalia Design Language |
| [`standards/shared-libraries.md`](standards/shared-libraries.md) | Which shared libraries exist and when to add one |
| [`.github/workflows/`](.github/workflows) | Reusable workflows: `rust-gate`, `git-sources`, `agents-check`, `packaging-lint`, `ast-grep`, `nix`, `freebsd` |
| [`scripts/`](scripts) | `check_pins.py` (every action pinned to a SHA) and `pin_actions.py` (pins tags to the commits they name today) |
| [`templates/`](templates) | `AGENTS.md`, `NODALIA_MIGRATION.md`, `SECURITY.md`, PR and issue templates, `renovate.json`, `.coderabbit.yaml`, a caller CI workflow |
| [`vendor/README.md`](vendor/README.md) | The libraries and build inputs that came from `storytold`, kept here with history and licences on `vendor/*` branches |
| [`status/ecosystem.md`](status/ecosystem.md) | Every repository: category, migration state, CI, NDL, independence, release |

## Using a shared workflow

Call it by full commit SHA, never a branch:

```yaml
jobs:
  gate:
    uses: getnodalia/foundation/.github/workflows/rust-gate.yml@<commit-sha> # foundation <date>
```

Renovate moves the pin in each repository. A change here reaches an app only when that app's pin
moves, so every app chooses when to take it and its own CI proves it.

## Changing this repository

`self-check.yml` runs actionlint and checks that every action is pinned to a SHA. A change to a
reusable workflow is tested by pointing one app's PR at the new commit before other apps move.

## Licence

The standards, workflows, scripts and templates on `main` are MIT OR Apache-2.0, written for
Nodalia; they contain no code from other organizations' workflow repositories. The vendored code on
the `vendor/*` branches keeps its own licences (see [`vendor/README.md`](vendor/README.md)).
