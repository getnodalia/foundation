//! The integration binary of nodalia-table: every test is a registered trial.

mod grid;
mod outline;
mod refpick;
mod slicer;

use nodalia_table::ui::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
