//! The nodalia-ui story viewer: the registered stories of the linked crates, shown under a chosen appearance.
#![warn(missing_docs)]

pub mod chrome;
pub mod viewer;

// The Foundations cards.
pub mod foundations;

// The mock editor window.
pub mod mock;

/// The gallery window's default size, in points.
pub const WINDOW: [f32; 2] = [1280.0, 800.0];

/// The registrations of every crate whose stories the viewer shows, by crate.
///
/// Each entry is a function of its crate that is passed by pointer, so the linker keeps that crate's object files and
/// the story registrations in them, which a release build for the web would otherwise drop.
type Registered = fn() -> Vec<&'static nodalia_ui::testing::Registration>;

#[allow(unused_mut, clippy::vec_init_then_push)]
fn crates() -> Vec<(&'static str, Registered)> {
    let mut crates: Vec<(&'static str, Registered)> = Vec::new();
    #[cfg(feature = "automation")]
    crates.push(("nodalia-automation", nodalia_automation::testing::registered));
    #[cfg(feature = "browse")]
    crates.push(("nodalia-browse", nodalia_browse::ui::testing::registered));
    #[cfg(feature = "color-ui")]
    crates.push(("nodalia-color-ui", nodalia_color_ui::ui::testing::registered));
    #[cfg(feature = "draw")]
    crates.push(("nodalia-draw", nodalia_draw::testing::registered));
    #[cfg(feature = "imaging")]
    crates.push(("nodalia-imaging", nodalia_imaging::testing::registered));
    #[cfg(feature = "layers")]
    crates.push(("nodalia-layers", nodalia_layers::testing::registered));
    #[cfg(feature = "menu")]
    crates.push(("nodalia-menu", nodalia_menu::testing::registered));
    #[cfg(feature = "pages")]
    crates.push(("nodalia-pages", nodalia_pages::testing::registered));
    #[cfg(feature = "print")]
    crates.push(("nodalia-print", nodalia_print::testing::registered));
    #[cfg(feature = "review")]
    crates.push(("nodalia-review", nodalia_review::testing::registered));
    #[cfg(feature = "table")]
    crates.push(("nodalia-table", nodalia_table::ui::testing::registered));
    #[cfg(feature = "text")]
    crates.push(("nodalia-text", nodalia_text::testing::registered));
    #[cfg(feature = "theme-editor")]
    crates.push(("nodalia-theme-editor", nodalia_theme_editor::testing::registered));
    #[cfg(feature = "theme-store")]
    crates.push(("nodalia-theme-store", nodalia_theme_store::ui::registered));
    #[cfg(feature = "timeline")]
    crates.push(("nodalia-timeline", nodalia_timeline::testing::registered));
    // These do not build for the web, so their stories are in the native gallery only.
    #[cfg(all(feature = "dialogs", not(target_arch = "wasm32")))]
    crates.push(("nodalia-dialogs", nodalia_dialogs::testing::registered));
    #[cfg(all(feature = "font-manager", not(target_arch = "wasm32")))]
    crates.push(("nodalia-font-manager", nodalia_font_manager::testing::registered));
    #[cfg(all(feature = "update", not(target_arch = "wasm32")))]
    crates.push(("nodalia-update", nodalia_update::testing::registered));
    std::hint::black_box(crates)
}

/// How many registrations each linked crate contributes, with the viewer's own, and how many stories there are in all.
pub fn linked_counts() -> (Vec<(&'static str, usize)>, usize) {
    let mut counts: Vec<(&'static str, usize)> = crates().into_iter().map(|(name, registered)| (name, registered().len())).collect();
    counts.push((env!("CARGO_PKG_NAME"), testing::registered().len()));
    (counts, nodalia_ui::testing::stories().len())
}

/// The test registry of this package's stories.
pub mod testing {
    nodalia_ui::testing_registered!();
}
