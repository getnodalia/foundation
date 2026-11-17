#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

//! The craft UI library: runtime, style, fonts, primitives, the component contract, layout, components, patterns and
//! the shell (layers 2 to 7).
//!
//! The library is built as crates along its layers: nodalia-ui-contract (runtime to contract, and the test kit),
//! nodalia-ui-widgets, nodalia-ui-panels, then nodalia-ui-canvas, nodalia-ui-patterns and nodalia-ui-shell side by side. This
//! crate re-exports all of them under one root, so every `nodalia_ui::…` path names the same item as in the crate that
//! defines it.
#![warn(missing_docs)]

pub use nodalia_ui_canvas::{canvas, canvas_controls, dialog};
#[cfg(feature = "testing")]
pub use nodalia_ui_contract::testing_registered;
#[doc(hidden)]
pub use nodalia_ui_contract::{__private, __register_command_set, __register_contract, __register_pattern};
pub use nodalia_ui_contract::{InstallError, InstallSpec, contract, fonts, install, layout, primitives, runtime, style, words};
pub use nodalia_ui_panels::{docking, rails, sections};
pub use nodalia_ui_shell::shell;
pub use nodalia_ui_widgets::{
    bars, buttons, choice, controls, display, edit, form, graph, layout_components, list, menu, notices, pickers, popover, table, tabs, text,
    tile_grid, value_drag,
};

/// `Inspector`, `CommandPalette`, `PreferencesWindow`, `DockArea`, `DockPanels`, `PanelSpec`,
/// `NavigatorPanel` and the other patterns.
pub mod patterns {
    pub use nodalia_ui_patterns::patterns::*;

    /// Canvas panel patterns: `NavigatorPanel`.
    pub mod canvas {
        pub use nodalia_ui_canvas::canvas::navigator_panel::{NavigatorPanel, NavigatorPanelOutput};
    }
}

/// The fixture, the suite runner and the story helpers of every crate of the library.
#[cfg(feature = "testing")]
pub mod testing {
    pub use nodalia_ui_canvas::testing::*;

    crate::testing_registered!();

    /// A crate's `registered`.
    type Registered = fn() -> Vec<&'static Registration>;

    /// The crates of the library, each with its `registered`.
    const LIBRARY: [(&str, Registered); 7] = [
        ("nodalia-ui", registered),
        ("nodalia-ui-contract", nodalia_ui_contract::testing::registered),
        ("nodalia-ui-widgets", nodalia_ui_widgets::testing::registered),
        ("nodalia-ui-panels", nodalia_ui_panels::testing::registered),
        ("nodalia-ui-canvas", nodalia_ui_canvas::testing::registered),
        ("nodalia-ui-patterns", nodalia_ui_patterns::testing::registered),
        ("nodalia-ui-shell", nodalia_ui_shell::testing::registered),
    ];

    /// Every registration declared in the library crates of the library: this crate and the six it re-exports.
    /// Types declared in integration binaries are fixtures and are left out.
    pub fn library_registrations() -> Vec<&'static Registration> {
        // A crate's registrations run only in a binary that links the crate; naming each crate's `registered`
        // links them all.
        let library = std::hint::black_box(LIBRARY);
        crate::contract::registrations()
            .into_iter()
            .filter(|registration| {
                library.iter().any(|(name, _)| *name == registration.crate_name())
                    && registration.crate_target() == registration.crate_name().replace('-', "_")
            })
            .collect()
    }
}
