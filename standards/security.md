# Security standard

## Reporting

Vulnerabilities in any Nodalia app are reported to **Nodalia**, through GitHub private
vulnerability reporting on the app's own repository
(`https://github.com/getnodalia/<repo>/security/advisories/new`). A `SECURITY.md` never points at
the project a codebase originally came from. Use `templates/SECURITY.md`.

When a report concerns code inherited from an upstream project, Nodalia fixes its own release
first and then tells the upstream maintainers privately, as a courtesy.

## Secrets

- Secrets live only in GitHub Actions secrets (repository or organization), never in files,
  variables, logs, error strings or issue text.
- A workflow passes a secret only to the step that uses it, and never to code from a fork
  (`pull_request_target` with a checkout of PR code is forbidden).
- Signing material (Apple, Windows, Linux package keys) is used only in release workflows behind a
  protected `release` environment.
- App credentials for third-party services (OAuth clients, music or mail APIs) are supplied at
  build time through `NODALIA_*`/app-prefixed variables, never committed.

## Supply chain

- Actions pinned to commit SHAs (`scripts/check_pins.py`).
- Cargo git dependencies only from `getnodalia/*` or reviewed independent upstreams, at a fixed
  `rev`; `git-sources.yml` enforces it. No `[patch]` or source replacement in `.cargo/config`.
- Lockfiles are committed and CI runs with `--locked`.
- New dependencies: licence on the allowlist (see [dependencies.md](dependencies.md)), maintained,
  and no install scripts that fetch from the network at build time unless documented.
- Release artifacts carry SHA-256 checksums; build provenance is attested with
  `actions/attest-build-provenance` where the release workflow supports it.

## Repository settings (per repository, free on public repos)

- Private vulnerability reporting: on.
- Secret scanning and push protection: on.
- Dependency graph and Dependabot **alerts**: on (alerts only; updates come from Renovate).
- Default `GITHUB_TOKEN` permission: read.
- Branch protection on the real default branch: PR required, required checks per [ci.md](ci.md).
