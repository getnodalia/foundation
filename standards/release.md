# Release and versioning

## Versions

- SemVer per app. `main` may carry a `-dev` pre-release; the release commit carries the plain version.
- A patch release need not ship on every platform or edition at once: a macOS-only fix can be
  `x.y.z` for macOS alone, and the release notes say so.
- When an app has a meaningful batch of changes, cut a release and update the website and README
  to match.
- Tags `vX.Y.Z` are pushed by a maintainer (agents cannot push tags). The release workflow builds
  from the tagged commit.

## Release pipeline (layer 3 of [ci.md](ci.md))

1. Resolve the version from the manifest; fail if the tag and the manifest disagree.
2. Build each platform from the same commit on standard runners.
3. Smoke-test each artifact: install or unpack it on a clean runner and launch the binary
   (`--version` or a headless run).
4. SHA-256 checksums for every artifact; attest provenance where supported.
5. Upload to a **draft** GitHub release on the app's own repository.
6. A maintainer reviews the draft and publishes.
7. After publishing: download the published assets, verify checksums, and check the website's
   download buttons resolve to them.

A failed platform blocks the draft unless the workflow has an explicit, documented
"draft without platform X" input that a maintainer chose for that run.

## Platforms

| Platform | Artifacts | Notes |
|---|---|---|
| Linux | AppImage, `.deb`, `.rpm`, tarball; Flatpak where the app has a manifest | built on `ubuntu-24.04`; smoke-tested on clean distro containers |
| macOS | one `.dmg` per edition, Apple Silicon (plus Intel or universal where the app supports it) | built on standard `macos-15` / `macos-26` runners (never `xlarge`); **unsigned and not notarised** (Nodalia has no Apple Developer ID); every DMG opens a designed install window with its own app-coloured background |
| Windows | MSI (and portable zip where useful), x64 and ARM64 | signed only if a free signing route is configured |

Updater endpoints point at `getnodalia/<repo>` GitHub releases or `getnodalia.com`. An app never
checks a third party's release feed.

## Website

App pages live at `getnodalia.com/<app>`. The download button detects the OS and offers the
latest release assets from GitHub. Update the page and the README in the release PR.
