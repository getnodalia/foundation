#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

//! The fixture faces as an app's crate sees them; read by `nodalia-fonts-build`'s tests.

use nodalia_fonts_build::{EmbeddedFace, ServedFace};

pub static NODALIA_FONTS: &[EmbeddedFace] = include!(concat!(env!("OUT_DIR"), "/nodalia_fonts.rs"));

pub static NODALIA_FONTS_SERVED: &[ServedFace] = include!(concat!(env!("OUT_DIR"), "/nodalia_fonts_served.rs"));
