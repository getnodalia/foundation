# Dependencies, licences and provenance

## Licence allowlist

Code dependencies and assets use SPDX identifiers. Allowed without review: `MIT`, `Apache-2.0`,
`BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `Zlib`, `Unicode-3.0`, `MPL-2.0` (unmodified),
`OFL-1.1`, `CC0-1.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`, public domain.

A repository may be stricter (its `deny.toml` or asset rules win). Apps under GPL or AGPL (Vinilo
GPL-3.0-or-later, Buzón AGPL-3.0-or-later) may use GPL-compatible dependencies; record each in the
app's licence document. Anything else needs Daniel's approval first.

A file with **no licence** is all rights reserved: never copy it, even into a workflow.

## Inherited code

Several Nodalia apps started from another open-source project. For each of them:

- Keep the original `LICENSE`, `NOTICE` and copyright lines. Credit the origin in `NOTICE` and the
  About window. Never claim it was written from scratch.
- Keep upstream history where it exists.
- Do not describe the app as a fork in the README, website or UI; the provenance lives in the legal
  files.
- An upstream library the app needs at build time is **vendored into `getnodalia/foundation`**
  with its history and licence, on a `vendor/<repo>/<branch>` branch, and depended on at a fixed
  `rev`. [`vendor/README.md`](../vendor/README.md) says where each came from and which upstream
  commit it was imported at.
- Upstream sync is a deliberate, reviewed merge through a rename tool (`scripts/rebrand.py` and a
  mirror branch), never an automatic push to the default branch.

## Vendored code

| Code | Upstream | Licence | Used by |
|---|---|---|---|
| craft-libs | storytold/craft-libs | MIT OR Apache-2.0 | the Rust desktop apps |
| egui | storytold/egui (emilk/egui) | MIT OR Apache-2.0 | the Rust desktop apps |
| winit | storytold/winit (rust-windowing/winit) | Apache-2.0 | the Rust desktop apps |
| craft-fonts | storytold/craft-fonts | per-font OFL/Apache; repository MIT OR Apache-2.0 | font build input |
| craft-i18n | storytold/craft-i18n | MIT OR Apache-2.0 | translations build input |
| winprint.rs | storytold/winprint.rs | BSD-3-Clause | Windows printing |
| indd-utils | storytold/indd-utils | MIT OR Apache-2.0 | Pliego |
| filmcraft | storytold/filmcraft | MIT OR Apache-2.0 | Pulso |

All of it lives in this repository; branches and pinned commits are in
[`vendor/README.md`](../vendor/README.md).

## Updates

Renovate, weekly, grouped by ecosystem, at most a handful of open PRs per repository. Security
updates are not grouped. Major versions get their own PR and a human review.
