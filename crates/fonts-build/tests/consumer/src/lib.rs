#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

//! The fixture faces as an app's crate sees them; read by `nodalia-fonts-build`'s tests.

use nodalia_fonts_build::{EmbeddedFace, ServedFace};

/// The faces the build script embedded.
pub static NODALIA_FONTS: &[EmbeddedFace] = include!(concat!(env!("OUT_DIR"), "/nodalia_fonts.rs"));

/// The faces the build script wrote for serving.
pub static NODALIA_FONTS_SERVED: &[ServedFace] = include!(concat!(env!("OUT_DIR"), "/nodalia_fonts_served.rs"));
