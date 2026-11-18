//! Vorbis I: the pure-Rust [`decoder`] (feature `vorbis-decode`) and [`encoder`] (feature
//! `vorbis-encode`). `nodalia_audio::decode` still reads Vorbis files through symphonia.

#[cfg(feature = "vorbis-decode")]
pub mod decoder;
#[cfg(feature = "vorbis-encode")]
pub mod encoder;
