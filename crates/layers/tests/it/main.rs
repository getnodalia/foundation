//! The integration binary of nodalia-layers: every test is a registered trial.

mod blend_rows;
mod comps;
mod panel_drag_menu;
mod panel_filter;
mod panel_input;
mod panel_order;
mod panel_reveal;
mod panel_rows;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &nodalia_layers::testing::registered());
}
