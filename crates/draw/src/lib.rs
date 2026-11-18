//! Vector and shape tools: gradient editing, the Pen and path editing, strokes and corners, shapes, slices, artboards and connectors, Crop and Perspective Crop, Free Transform, measure, symmetry and brush presets.
#![warn(missing_docs)]

pub mod geometry;
pub mod stroke;
#[cfg(feature = "ui")]
pub mod ui;

#[cfg(feature = "screen-testing")]
pub mod testing {
    //! The registrations of this crate's stories, for the `tests/it` harness.
    nodalia_ui::testing_registered!();
}

#[cfg(all(test, feature = "screen-testing"))]
extern crate self as nodalia_draw;
#[cfg(all(test, feature = "screen-testing"))]
#[path = "../tests/it/main.rs"]
mod integration;

#[cfg(test)]
fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &nodalia_ui::testing::registered_in(env!("CARGO_PKG_NAME")));
}
