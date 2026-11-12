# CI/CD standard

Every Nodalia repository builds, tests and releases on **standard GitHub-hosted runners only**.
No Blacksmith, no GetMac, no larger runners (`macos-*-xlarge`, `*-large`), no self-hosted or home
runners, no personal computers, no paid trials. A workflow that cannot run that way is not merged.

## Three layers

| Layer | When | What | Rules |
|---|---|---|---|
| 1. PR validation | every PR and push to the default branch | format, lint, build or type check, unit tests, `git-sources`, agent instructions, workflow lint | fast (target under 20 min); Linux only unless the change is platform code; cancels superseded PR runs |
| 2. Deep validation | nightly, pushes to `release`, and PRs that touch the platform's own files | integration and regression tests, platform matrix (macOS, Windows, Windows ARM64, FreeBSD), packaging smoke tests, Nix evaluation, licence audit, CodeQL, Scorecard | path-filtered so an unrelated PR never queues macOS; never required on ordinary PRs |
| 3. Release | manual dispatch or push to `release`; tags are pushed by a maintainer | build from an immutable commit, checksums, signing/notarisation when configured, install and launch tests, draft release, publish after review | never cancelled; publishes only when every required platform built and passed its smoke test |

## Shared workflows

Reusable workflows live in this repository under `.github/workflows/`. Call them by **full commit
SHA** with a version comment, never `@main`:

```yaml
jobs:
  gate:
    uses: getnodalia/foundation/.github/workflows/rust-gate.yml@<sha> # foundation 2026-11-12
    with:
      packages: pkg-config libxkbcommon-dev
```

| Workflow | Replaces | Purpose |
|---|---|---|
| `rust-gate.yml` | the inherited `gate.yml` | toolchain, apt packages, cargo tools, optional fonts/translations inputs, `cargo xtask ci` (or another command), lockfile unchanged |
| `git-sources.yml` | inline "Git dependencies come from storytold" jobs | every git dependency comes from an allowed owner; no cargo source replacement |
| `agents-check.yml` | the inherited `house-rules.yml` | `AGENTS.md` follows [the agents standard](agents.md) and carries no inherited rule block |
| `packaging-lint.yml` | the inherited `packaging-lint.yml` | actionlint, shellcheck, desktop-file-validate, appstreamcli |
| `ast-grep.yml` | the inherited `ast-grep.yml` | ast-grep rule tests and scan |
| `nix.yml` | the inherited `nix.yml` | `nix flake check --no-build` |
| `freebsd.yml` | the inherited `freebsd.yml` | build and test in a FreeBSD VM on a Linux runner (x86_64; nightly) |

Workflows that only one product needs (Lienzo's perf nightly, Vortia's numerical checks, Nodalix
OS's ISO and kernel builds) stay in that product's repository. Move a job here only when a second
repository needs the same thing.

## Rules for every workflow

- `permissions: contents: read` at the top; widen per job only where needed.
- Every `uses:` is a full 40-character SHA plus `# vX.Y.Z`. `scripts/check_pins.py` checks it.
- `actions/checkout` with `persist-credentials: false` unless the job pushes.
- PR runs: `concurrency` with `cancel-in-progress` for pull requests only. Release runs never cancel.
- Caches: Swatinem/rust-cache (or the language's own); PRs read the default branch's cache and
  never save their own.
- Job and check names are stable: a renamed check breaks branch protection.
- No check that always passes, no `continue-on-error` on a gate, no skipped tests to get green.
- macOS: the organization has 5 concurrent macOS slots in total. A PR workflow that needs macOS is
  path-filtered to the files that can break it. Prefer one universal build over separate arm64 and
  x86_64 jobs.
- Private repositories: check the plan's included minutes before adding a scheduled job.

## Required checks

Add a check to branch protection only after it has passed on the default branch and on a
representative PR, runs on every PR it applies to (no path filter that leaves it pending), and
fails for real reasons. Start with the layer-1 gate. SonarCloud, CodeQL, Scorecard and CodeRabbit
inform reviews; they do not replace tests.

## Quality services

- **SonarCloud**: Automatic Analysis, organization `getnodalia`, key `getnodalia_<repo>`.
  `.sonarcloud.properties` for exclusions. No CI scan workflow (Automatic Analysis rejects it).
- **CodeQL**: `codeql.yml` per repository with the languages it really has, `build-mode: none`
  where supported.
- **OpenSSF Scorecard**: scheduled and on default-branch pushes.
- **CodeRabbit**: free for public repositories; configured by `.coderabbit.yaml` (template in
  `templates/`). Its findings are suggestions until a human confirms them.
- **Dependency updates**: Renovate, weekly and grouped, one bot per ecosystem. Dependabot is not used.
