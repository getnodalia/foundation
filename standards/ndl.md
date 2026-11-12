# NDL integration contract

The Nodalia Design Language lives in [`getnodalia/nodalia-design`](https://github.com/getnodalia/nodalia-design).
Its `docs/status.md` is the source of truth for what is verified. This page says how an app
consumes it.

## Packages by toolkit

| App toolkit | Package | How it is consumed |
|---|---|---|
| GTK4 (Rust) | `nodalia-gtk` crate (`packages/gtk/crate`), `use nodalia_gtk as ndl;` | git dependency pinned by `rev`; no libadwaita, no relm4 `gnome_*`/`libadwaita` features |
| egui (Rust) | `nodalia-theme` crate (`packages/egui/crate`) | git dependency pinned by `rev`, or vendored under `vendor/nodalia-theme` with a `VENDORED.md` naming the commit |
| Qt Widgets / Qt Quick | `@nodalia/qtwidgets`, `@nodalia/qml` generated sheets | generated files copied in with the commit they came from |
| Web | `@nodalia/web`, `@nodalia/tokens` CSS | npm package at a fixed version |
| Icons | `@nodalia/icons` | generated set, never redrawn per app |
| Updates | `nodalia-update` crate (`packages/update/crate`) | shared update check and dialog contract |

Never copy NDL source files into an app by hand. A widget NDL lacks is added to `nodalia-design`
first, then the app's pin moves.

## Identity rules

- Colours come only from NDL tokens (`--ndl-*`, `Tokens`), plus the app's own accent, defined in
  `nodalia-design`'s per-app accent table.
- Hamburger menu in the header: Preferences, Keyboard shortcuts, About. No Preferences button in
  the sidebar. The light/dark selector lives only in Preferences.
- Round 28 px window controls drawn by NDL **on Linux only**, unless the user picks the desktop's
  own in Preferences. macOS and Windows use native window controls.
- Dialogs use NDL controls (Preferences: close only), never a GNOME titlebar.
- Linux apps export their menu over D-Bus to the shell's global menu; the in-window menu bar shows
  only when the desktop has no global menu.
- No decorative gradients or glows. No redundant hover tooltips.

## Platforms

- **Linux**: NDL is the visual language.
- **macOS**: an app may ship an NDL edition and a native SwiftUI edition (Liquid Glass, built with
  the macOS 26 SDK). Both share the engine (Rust core, sidecar or library); only the UI differs.
- **Windows**: NDL adapted to Windows conventions (native window controls, Windows menus).
- **Nodalix OS** is the exception: its shell and system apps are GNOME/Adwaita. Nodalia identity
  goes into wallpapers, icons, accent and extensions, never by replacing GNOME components with NDL.

## Per-app status

Each app's `AGENTS.md` (section "NDL") and `NODALIA_MIGRATION.md` say what is integrated and what
is left.
