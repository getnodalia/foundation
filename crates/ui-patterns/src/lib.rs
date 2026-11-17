#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

//! The patterns of the craft UI library: ready-made dialogs, presets, preferences, dock areas and panels (layer 6).
//!
//! The root re-exports nodalia-ui-panels' modules and the ones it re-exports.
#![warn(missing_docs)]

// The derives' output names the crate as `nodalia_ui`, here as in every other crate.
extern crate self as nodalia_ui;

#[doc(hidden)]
pub use nodalia_ui_panels::canvas_data;
#[cfg(feature = "testing")]
#[doc(hidden)]
pub use nodalia_ui_panels::story_kit;
#[cfg(feature = "testing")]
pub use nodalia_ui_panels::testing_registered;
#[doc(hidden)]
pub use nodalia_ui_panels::{__private, __register_command_set, __register_contract, __register_pattern};
pub use nodalia_ui_panels::{InstallError, InstallSpec, contract, fonts, install, layout, primitives, runtime, style, words};
pub use nodalia_ui_panels::{
    bars, buttons, choice, controls, display, edit, form, graph, layout_components, list, menu, notices, pickers, popover, table, tabs, text,
    tile_grid, value_drag,
};
pub use nodalia_ui_panels::{dialog, docking, rails, sections};

pub mod patterns;

/// The fixture, the suite runner and the story helpers.
#[cfg(feature = "testing")]
pub mod testing {
    pub use nodalia_ui_panels::testing::*;

    crate::testing_registered!();
}
