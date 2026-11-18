# craft

The craft libraries in one dependency. An app pins one revision of this crate and turns on features; everything is imported as `craft::<crate>`.

```toml
[workspace.dependencies]
craft = { git = "https://github.com/getnodalia/foundation", rev = "…" }

# crates/ui-egui/Cargo.toml
craft = { workspace = true, features = ["ui", "color-ui", "draw", "imaging", "keymap", "platform-appearance"] }
```

## Always on

`craft::theme`, `craft::i18n`, `craft::host`.

## Features

- One feature per crate, named after the crate without `craft-`: `color-ui` turns on `nodalia-color-ui` and re-exports it as `craft::color_ui`.
- `ui` turns on `nodalia-ui` (`craft::ui`), re-exports `egui` (`craft::egui`, the egui the library is built with) and forwards `ui` to every enabled crate.
- `screen-testing` implies `ui` and forwards to every enabled crate.
- Each crate feature is forwarded as `<crate>-<feature>` (`platform-appearance`, `text-hyphen`, `ui-window-frame`).
- A crate whose `ui` needs another family's `ui` turns that family's feature on (`draw` turns on `color-ui`).

The `[features]` table in `Cargo.toml` is written by `tests/features.rs` from the member crates' manifests. After changing a member's features or adding a crate, run `UPDATE_FACADE=1 cargo test -p craft -- integration::features` and commit the result. A comment on a feature line marks a crate that does not build for `wasm32-unknown-unknown`.

Reached through other crates, not named in the facade: the six library crates (`nodalia-ui-contract` to `nodalia-ui-shell`), `nodalia-ui-macros` and `nodalia-behavior` through `nodalia-ui`, and `nodalia-win32` through `nodalia-window`.

Not in the facade, because they are tools or test harnesses: `nodalia-ui-gallery`, `story-render`, `feature-root` (the features local builds resolve with), `nodalia-ui-bench`, `nodalia-ui-test-kit`, `nodalia-fonts-build` (a build-script helper), `nodalia-design-lint`, `nodalia-plate-test`, `nodalia-media-testkit`, `nodalia-render-parity`.

## Family dependencies

`tests/families.rs` fails when one family crate's `ui` depends on another family crate's `ui`. `nodalia-color-ui` is the base family that any family may use.

## egui fork

`craft::egui_fork::{GIT, REV}` name the egui fork the library is built with, and `check_lockfile(lock)` checks that an app's `Cargo.lock` takes every egui package from it. An app's xtask calls it in its `ci` and `check` commands. The app's workspace must also patch egui to this fork, since `[patch]` applies only at the workspace root.
