//! Stories of `FilterButton`: plain, filtered and sorted.

use super::FilterButton;
use nodalia_behavior::ColumnKey;
use nodalia_ui::contract::{ColumnSort, Show as _};
use nodalia_ui::testing::{Drive, StoryData, StoryOutput, story};
use egui::Ui;

#[story(FilterButton, covers = [Default], drive = Drive::Activate)]
fn filter_button(ui: &mut Ui, _: &mut StoryData) -> StoryOutput {
    FilterButton::new("Colour").show(ui).into()
}

#[story(FilterButton, covers = [], drive = Drive::Activate)]
fn filter_button_filtered(ui: &mut Ui, _: &mut StoryData) -> StoryOutput {
    FilterButton::new("Colour").filtered(true).show(ui).into()
}

#[story(FilterButton, covers = [], drive = Drive::Activate)]
fn filter_button_sorted(ui: &mut Ui, _: &mut StoryData) -> StoryOutput {
    FilterButton::new("Colour").sort(ColumnSort::descending(ColumnKey::new("colour"))).show(ui).into()
}
