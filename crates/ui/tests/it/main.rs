//! The integration binary of nodalia-ui: every test is a registered trial.

mod api_map;
mod canvas;
mod components_index;
mod form_dialogs;

mod shell;

use nodalia_ui::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
