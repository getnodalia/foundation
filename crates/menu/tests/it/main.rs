//! The integration binary of nodalia-menu: every test is a registered trial.

mod layout;
mod mnemonic;
mod native;
mod sample;
mod shortcuts;

fn main() {
    nodalia_ui::testing::run(module_path!(), env!("CARGO_PKG_NAME"), &nodalia_menu::testing::registered());
}
