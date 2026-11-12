# Ecosystem status

Every state here is backed by a PR, a CI run or a file in the repository; anything not verified
says **pending**. Updated with each Foundation PR.

Last update: 2026-11-12.

## Definitions

- **Migración completa** (priority apps): development and release depend only on Nodalia; no
  required `storytold/*` dependency; own workflows; CI passing; NDL integrated for the platform;
  releases build on free runners; features preserved; AGENTS.md and docs current; updaters point
  at valid infrastructure; essential tests pass; third-party licences kept; result checked on the
  available platforms.
- **Base Nodalia preparada** (secondary apps): own standards and docs, basic CI working, specific
  AGENTS.md, NDL strategy, detailed `NODALIA_MIGRATION.md`, inherited dependencies identified.

## Priority apps

| Repository | Category | Status | CI | NDL | Independence | Release |
|---|---|---|---|---|---|---|
| [vinilo](https://github.com/getnodalia/vinilo) | Priority | pending | own workflows; actions pinned in [#69](https://github.com/getnodalia/vinilo/pull/69) | GTK client on `nodalia-gtk`; two macOS editions (Nodalia, Native SwiftUI) | no `storytold` reference in the repository | own `release.yml` (Linux, two macOS DMGs) |
| [vortia](https://github.com/getnodalia/vortia) | Priority | pending | own workflows; action pins pending (after the v0.7.0 release run) | Qt Widgets on `@nodalia/qtwidgets`; Rust/egui port in progress | no `storytold` reference | own `release-appimage.yml` |
| [forja](https://github.com/getnodalia/forja) | Priority | pending | gate, packaging lint, Nix, FreeBSD, Windows ARM64 and release still call `storytold/craft-common-actions` | egui on `nodalia-theme` (vendored) | Cargo git deps on `storytold/craft-libs`, `egui`, `winit`; fonts from `storytold/craft-fonts` | release delegated to `storytold` (unusable: its secrets and paid macOS runner); macOS DMG built by own `macos.yml` |
| [nodalix-os](https://github.com/getnodalia/nodalix-os) | Operating system | pending | own workflows; actions pinned in [#102](https://github.com/getnodalia/nodalix-os/pull/102) | GNOME/Adwaita by design (exception in [ndl.md](../standards/ndl.md)) | ArtCraft launcher (downloaded from a `storytold` release) removed in [#103](https://github.com/getnodalia/nodalix-os/pull/103) | own ISO, kernel, NxPM and repository workflows |
| [lienzo](https://github.com/getnodalia/lienzo) | Priority | pending | gate, house rules, packaging lint, Nix, FreeBSD, Windows ARM64 call `storytold/craft-common-actions`; apt action from it | egui NDL (Nodalia design merged) | Cargo git deps on `storytold/craft-libs`, `egui`, `winit`, `winprint.rs`; fonts from `storytold/craft-fonts` | own `release-linux/macos/windows.yml` (fonts still from `storytold`) |

## Secondary apps

| Repository | Origin | Status | Inherited dependencies |
|---|---|---|---|
| [torno](https://github.com/getnodalia/torno) | SolidCraft (tangency-labs) | pending | CI fonts checkout and Arch packaging action from `storytold` |
| [celdas](https://github.com/getnodalia/celdas) | GridCraft | pending | shared workflows; `craft-libs`, `egui`, `winit`, `winprint.rs` |
| [lamina](https://github.com/getnodalia/lamina) | DeckCraft | pending | shared workflows; `craft-libs`, `egui`, `winit` |
| [letra](https://github.com/getnodalia/letra) | WordCraft | pending | shared workflows; `craft-libs`, `egui`, `winit`, `winprint.rs`; `craft-i18n` |
| [luz](https://github.com/getnodalia/luz) | LightCraft | pending | shared workflows; `craft-libs`, `egui`, `winit` |
| [papel](https://github.com/getnodalia/papel) | PdfCraft | pending | shared workflows; `craft-libs`, `egui`, `winit`, `winprint.rs`; `craft-i18n` |
| [pliego](https://github.com/getnodalia/pliego) | DesignCraft | pending | shared workflows; `craft-libs`, `egui`, `winit`, `winprint.rs`, `indd-utils` |
| [pluma](https://github.com/getnodalia/pluma) | VectorCraft | pending | shared workflows; `craft-libs`, `egui`, `winit`, `winprint.rs` |
| [pulso](https://github.com/getnodalia/pulso) | EffectCraft | pending | shared workflows; `craft-libs`, `egui`, `winit`, `filmcraft` |
| [toma](https://github.com/getnodalia/toma) | FilmCraft | pending | shared workflows; `craft-libs`, `egui`, `winit` |
| [brujula](https://github.com/getnodalia/brujula) | GNOME Web (Epiphany) | pending | none from `storytold` |
| [tienda](https://github.com/getnodalia/tienda) | Bazaar | pending | none from `storytold` |
| [buzon](https://github.com/getnodalia/buzon) | Hylki | pending | none from `storytold` |
| [lumbre](https://github.com/getnodalia/lumbre) | Nodalia | pending | not audited yet |

## Shared libraries, infrastructure and auxiliary repositories

| Repository | Category | Notes |
|---|---|---|
| [nodalia-design](https://github.com/getnodalia/nodalia-design) | Shared library | NDL tokens, toolkit packages, icons, `nodalia-update`; its `docs/status.md` is the verified state |
| [foundation](https://github.com/getnodalia/foundation) | Infrastructure | this repository |
| [.github](https://github.com/getnodalia/.github) | Infrastructure | organization profile |
| [nodalia-web](https://github.com/getnodalia/nodalia-web) | Website | `getnodalia.com` |
| [nodalix-icon-theme](https://github.com/getnodalia/nodalix-icon-theme) | Assets | icon and cursor theme |
| linux-nodalix (personal account) | Operating system | Nodalix OS kernel packaging |
| demo-repository | Auxiliary (private) | demo only |

## Vendored code

| Code | Status |
|---|---|
| craft-libs, egui, winit, craft-fonts, craft-i18n, winprint.rs, indd-utils, filmcraft | being imported into this repository with history ([`vendor/README.md`](../vendor/README.md)); no app points at it yet |

## Common and per-product

Common: the standards, the reusable workflows in this repository, `nodalia-design` packages,
`SECURITY.md`, PR template, Renovate config. Per-product exceptions, each with its reason, live in
the product's `AGENTS.md`: Nodalix OS keeps GNOME/Adwaita and its own ISO/kernel pipelines;
Vinilo keeps its sidecar and two macOS editions; Vortia keeps its numerical test suite; Lienzo
keeps its perf nightly.
