//! The integration binary of nodalia-ui-shell: every test is a registered trial.

// The test files name the library as `nodalia_ui`, as the crates that use it do.
extern crate nodalia_ui_shell as nodalia_ui;

pub(crate) mod body;
mod commands;
mod contract;
mod dialog;
mod measure;
mod notices;

mod shell;

use nodalia_ui::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
