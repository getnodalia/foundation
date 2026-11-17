//! The integration binary of nodalia-ui-patterns: every test is a registered trial.

// The test files name the library as `nodalia_ui`, as the crates that use it do.
extern crate nodalia_ui_patterns as nodalia_ui;

mod blend_keys;
mod docking;
mod form_dialogs;

// Panels family.
mod panels;

mod preferences;
mod presets;

use nodalia_ui::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
