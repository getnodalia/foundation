//! The integration binary of nodalia-ui-contract: every test is a registered trial.

// The test files name the library as `nodalia_ui`, as the crates that use it do.
extern crate nodalia_ui_contract as nodalia_ui;

mod access;
pub(crate) mod body;
mod canvas;
mod collection;
mod contract;
mod drag;
mod egui_surface;
mod fonts;
mod icon_ids;
mod keys_consumed;
mod layout;
mod motion;
mod paint;

mod runtime;

mod style;
mod text;

use nodalia_ui::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
