//! The integration binary of nodalia-font-manager: every test is a registered trial.

mod missing;
mod panel;
mod picker;

use nodalia_font_manager::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
