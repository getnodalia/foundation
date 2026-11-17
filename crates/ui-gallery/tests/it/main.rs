//! The viewer's integration tests: one binary, run by `libtest-mimic` over the registered trials.

mod mock;
mod overview;
mod viewer;

use nodalia_ui_gallery::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
