//! Stories of `LayersOptionsDialog`.

use super::{LayersOptions, LayersOptionsDialog};
use nodalia_ui::contract::ShowContainer as _;
use nodalia_ui::dialog::{DialogStack, StackDialog as _};
use nodalia_ui::layout_components::Stack;
use nodalia_ui::testing::{Drive, StoryData, StoryOutput, story};
use egui::Ui;

#[story(LayersOptionsDialog, covers = [Open], drive = Drive::Never)]
fn open(ui: &mut Ui, data: &mut StoryData) -> StoryOutput {
    let options = data.value("options", LayersOptions::default());
    let mut dialog = LayersOptionsDialog::new(options.clone());
    let shown = Stack::new().show(ui, |ui, _| {
        let _ = dialog.show(ui, &DialogStack::default());
    });
    *options = dialog.options;
    shown.output.into()
}
