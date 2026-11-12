//! ISO BMFF (MP4) and QuickTime (MOV) demuxer and muxer: a re-export of
//! [`nodalia_media::isobmff`] from nodalia-libs. Supported boxes and limitations are in the
//! nodalia-media README.

#![cfg_attr(not(test), deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable))]

pub use nodalia_media::isobmff::*;
