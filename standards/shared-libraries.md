# Shared libraries

A new shared repository is created only when at least two apps need the same code and that code
has no better home. Today:

| Need | Where it lives | Notes |
|---|---|---|
| Design tokens, widgets, icons, fonts | `getnodalia/nodalia-design` | packages per toolkit (see [ndl.md](ndl.md)) |
| Update check and update dialog | `nodalia-design/packages/update` (`nodalia-update` crate) | one contract for every app's updater |
| Window, UI helpers, PDF, docpath, web host (Rust desktop apps) | craft-libs, vendored in `getnodalia/foundation` | inherited; crates are renamed only when all the apps move together |
| Fonts build input | craft-fonts, vendored in `getnodalia/foundation` | never committed into app repositories |
| Translations build input | craft-i18n, vendored in `getnodalia/foundation` | pinned per app by `craft-i18n.rev` |
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
