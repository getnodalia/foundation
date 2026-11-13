# Release and versioning

## Versions

- SemVer per app. `main` may carry a `-dev` pre-release; the release commit carries the plain version.
- A patch release need not ship on every platform or edition at once: a macOS-only fix can be
  `x.y.z` for macOS alone, and the release notes say so.
- When an app has a meaningful batch of changes, cut a release and update the website and README
  to match.
- Nobody pushes tags by hand. A release starts when a version bump lands on the default branch
  with its hand-written notes, `docs/release-notes/vX.Y.Z.md`: Foundation's `release-tag.yml`
  tags that commit and drafts the release with the notes as its body (see the pipeline below).

## Release pipeline (layer 3 of [ci.md](ci.md))

1. On every push to the default branch, `release-tag.yml` reads the version from the manifest. When
   it is a release version, is not tagged yet and has its notes file, it tags the pushed commit
   and creates a **draft** release whose body is the notes file. Otherwise it does nothing.
2. The same run calls the app's packaging workflows with the tag (`workflow_call`; a tag pushed
   with `GITHUB_TOKEN` starts no other workflow). Each builds from the tagged commit on standard
   runners and fails if the tag and the manifest disagree.
3. Smoke-test each artifact: install or unpack it on a clean runner and launch the binary
   (`--version` or a headless run).
4. SHA-256 checksums for every artifact; attest provenance where supported.
5. Upload to the draft release on the app's own repository.
6. `release-publish.yml` runs after every packaging job and publishes the draft. If any platform
   failed, the release stays a draft for a maintainer to look at.
7. After publishing: download the published assets, verify checksums, and check the website's
   download buttons resolve to them.

The caller, in each app (`.github/workflows/release-auto.yml`):

```yaml
on:
  push:
    branches: [main]
  # A draft whose packaging failed: fix it, then run this by hand with retag-draft.
  workflow_dispatch:
    inputs:
      retag-draft:
        type: boolean
        default: false
permissions:
  contents: read
concurrency:
  group: release-auto
  cancel-in-progress: false
jobs:
  tag:
    permissions:
      contents: write
    uses: getnodalia/foundation/.github/workflows/release-tag.yml@<sha>
    with:
      name: Lienzo
      notes-check: scripts/check-release-notes.sh
      retag-draft: ${{ inputs.retag-draft == true }}
  linux:
    needs: tag
    if: needs.tag.outputs.created == 'true'
    permissions:
      contents: write
    uses: ./.github/workflows/release-linux.yml
    with:
      tag: ${{ needs.tag.outputs.tag }}
  publish:
    needs: [tag, linux]
    permissions:
      contents: write
    uses: getnodalia/foundation/.github/workflows/release-publish.yml@<sha>
    with:
      tag: ${{ needs.tag.outputs.tag }}
```

When a platform fails and the fix lands after the tag, run the caller by hand on the fixed commit
with `retag-draft`: while the release is still a draft, its tag moves to that commit and every
platform builds again. A published release keeps its tag.

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
