//! The integration binary of nodalia-ui-canvas: every test is a registered trial.

// The test files name the library as `nodalia_ui`, as the crates that use it do.
extern crate nodalia_ui_canvas as nodalia_ui;

mod canvas;
mod canvas_controls;
mod contract;
// full-window parts
mod full_window_parts;
// end of full-window parts

use nodalia_ui::testing::registered;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &registered());
}
