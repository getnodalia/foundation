//! Matroska (MKV) and WebM demuxer and muxer: a re-export of [`nodalia_media::matroska`] from
//! nodalia-libs. Supported elements and limitations are in the nodalia-media README.

#![cfg_attr(not(test), deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable))]

pub use nodalia_media::matroska::*;
