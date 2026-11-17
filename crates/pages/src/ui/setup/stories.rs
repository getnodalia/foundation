//! Stories of the page setup dialog and the layout menus.

use super::{PageLayoutMenus, PageSetupDialog};
use crate::setup::PageSetup;
use nodalia_ui::buttons::IconButton;
use nodalia_ui::contract::{Bind, Props as _, Show as _};
use nodalia_ui::runtime::env::UnitKind;
use nodalia_ui::testing::{Drive, StoryData, StoryOutput, story};
use egui::Ui;

#[story(PageSetupDialog<'static>, covers = [], drive = Drive::Never)]
fn page_setup(ui: &mut Ui, data: &mut StoryData) -> StoryOutput {
    let setup = data.value("setup", PageSetup::default());
    PageSetupDialog::new(Bind::bound(setup)).layout().direction().opened(Bind::given(true)).show(ui);
    StoryOutput::default()
}

#[story(PageSetupDialog<'static>, covers = [], drive = Drive::Never)]
fn document_setup(ui: &mut Ui, data: &mut StoryData) -> StoryOutput {
    let start = PageSetup { pages: Some(8), mirrored: true, ..PageSetup::default() };
    let setup = data.value("setup", start);
    PageSetupDialog::new(Bind::bound(setup)).document_setup().unit(UnitKind::Millimetres).opened(Bind::given(true)).show(ui);
    StoryOutput::default()
}

#[story(PageLayoutMenus<'static>, covers = [Open], drive = Drive::Never)]
fn margins_menu(ui: &mut Ui, data: &mut StoryData) -> StoryOutput {
    let setup = data.value("setup", PageSetup::default()).clone();
    let opener = IconButton::new(nodalia_ui::controls::disclosure::DisclosureGlyph::menu_button()).label("Margins").show(ui);
    PageLayoutMenus::new(&setup).opened(Bind::given(true)).margins(ui, &opener);
    StoryOutput::default()
}
