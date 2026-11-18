# Shared libraries

A new shared repository is created only when at least two apps need the same code and that code
has no better home. Today:

| Need | Where it lives | Notes |
|---|---|---|
| Design tokens, widgets, icons, fonts | `getnodalia/nodalia-design` | packages per toolkit (see [ndl.md](ndl.md)) |
| Update check and update dialog | `nodalia-design/packages/update` (`nodalia-update` crate) | one contract for every app's updater |
| Window, UI helpers, PDF, docpath, web host (Rust desktop apps) | `nodalia-*` crates on `nodalia/libs` in `getnodalia/foundation` | generated from the upstream mirror; see [vendor/README.md](../vendor/README.md) |
| Fonts build input | `nodalia/fonts` in `getnodalia/foundation` (`NODALIA_FONTS_DIR`) | never committed into app repositories |
| Translations build input | `nodalia/i18n` in `getnodalia/foundation` (`NODALIA_I18N_DIR`) | pinned per app by `nodalia-i18n.rev` |
| CI/CD | this repository | reusable workflows |

Not created, and why:

- **Preferences/configuration, logging, error handling**: each app already has a working model
  that fits its toolkit (GTK `KeyFile`, egui serde state, Qt settings). A common crate would wrap
  them without removing any code. Revisit when two apps share the same storage format.
- **Telemetry**: Nodalia apps collect none. Local diagnostics stay in each app's log.
- **Installer/app store integration**: `getnodalia/tienda` is the store; apps expose standard
  AppStream metadata rather than a library.
- **Inter-component messaging**: Vinilo's NDJSON sidecar protocol and the egui apps' control
  channel are app-specific contracts; keep them in their apps.

Shared code never depends on an app, and no two shared repositories depend on each other in a
cycle.
