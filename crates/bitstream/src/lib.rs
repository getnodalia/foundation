//! Bit-level reading and writing: a re-export of [`nodalia_media::bitstream`] from nodalia-libs.

#![cfg_attr(not(test), deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable))]

pub use nodalia_media::bitstream::*;
