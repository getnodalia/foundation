//! The Craft App Suite as releases know it: each app's id, name and repository.
//!
//! An app that updates itself takes its own entry (`suite::PHOTOCRAFT`); the launcher takes all
//! of them. Installers use the list to tell a Craft App's package from anyone else's.

use crate::app::App;

/// Lienzo, the image editor.
pub const PHOTOCRAFT: App = App::new("photocraft", "Lienzo", "Image editing", "storytold/photocraft");
/// Pluma, the vector illustration app.
pub const VECTORCRAFT: App = App::new("vectorcraft", "Pluma", "Vector illustration", "storytold/vectorcraft");
/// Toma, the video editor.
pub const FILMCRAFT: App = App::new("filmcraft", "Toma", "Video editing, color and sound", "storytold/filmcraft");
/// Luz, the photo library and raw developer.
pub const LIGHTCRAFT: App = App::new("lightcraft", "Luz", "Photo library and raw development", "storytold/lightcraft");
/// Papel, the PDF reader and organizer (formerly PrintCraft).
pub const PDFCRAFT: App = App {
    former_ids: &["printcraft"],
    former_names: &["PrintCraft"],
    ..App::new("pdfcraft", "Papel", "Reading, organizing and protecting PDFs", "storytold/pdfcraft")
};
/// Pulso, the motion graphics app.
pub const EFFECTCRAFT: App = App::new("effectcraft", "Pulso", "Motion graphics and visual effects", "storytold/effectcraft");
/// Pliego, the page layout app.
pub const DESIGNCRAFT: App = App::new("designcraft", "Pliego", "Page layout and publishing", "storytold/designcraft");
/// Trama, the interface design app.
pub const FIGCRAFT: App = App::new("figcraft", "Trama", "Interface design and prototyping", "storytold/figcraft");
/// Letra, the writing and document design app.
pub const WORDCRAFT: App = App::new("wordcraft", "Letra", "Writing and document design", "storytold/wordcraft");
/// SoundCraft, the audio app.
pub const SOUNDCRAFT: App = App::new("soundcraft", "SoundCraft", "Recording, editing and mixing audio", "storytold/soundcraft");
/// Lámina, the presentation app.
pub const DECKCRAFT: App = App::new("deckcraft", "Lámina", "Presentations and slide shows", "storytold/deckcraft");
/// Forja, the computer-aided design app.
pub const CADCRAFT: App = App::new("cadcraft", "Forja", "Computer-aided design and drafting", "storytold/cadcraft");
/// Celdas, the spreadsheet app.
pub const GRIDCRAFT: App = App::new("gridcraft", "Celdas", "Spreadsheets and data", "storytold/gridcraft");

/// ArtCraft Launcher, described like a Craft App so it updates itself with the same machinery
/// (asset names `artcraft-launcher-<ver>-…`, bundle id `ai.storyteller.artcraft-launcher`,
/// `ArtCraft Launcher.app`). Not part of [`SUITE`].
pub const LAUNCHER: App = App::new("artcraft-launcher", "ArtCraft Launcher", "Installs and updates the Craft App Suite", "storytold/craft-launcher");

/// The Craft App Suite, in getartcraft.com's display order.
pub const SUITE: [App; 13] = [
    PHOTOCRAFT,
    VECTORCRAFT,
    FILMCRAFT,
    LIGHTCRAFT,
    PDFCRAFT,
    EFFECTCRAFT,
    DESIGNCRAFT,
    FIGCRAFT,
    WORDCRAFT,
    SOUNDCRAFT,
    DECKCRAFT,
    CADCRAFT,
    GRIDCRAFT,
];

/// The suite's app with this id.
pub fn by_id(id: &str) -> Option<&'static App> {
    SUITE.iter().find(|a| a.id == id)
}
