//! The integration binary of nodalia-ui-panels: every test is a registered trial.

// The test files name the library as `nodalia_ui`, as the crates that use it do.
extern crate nodalia_ui_panels as nodalia_ui;

mod access;
pub(crate) mod body;
mod dialogs;
mod dock_group;
// outer edit
mod edit;
// end of outer edit
mod focus;
mod internals;
mod list;
mod popup_surface;

mod rails;
mod sections;

use nodalia_ui::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
