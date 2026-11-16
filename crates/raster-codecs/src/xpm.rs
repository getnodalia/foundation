//! XPM compatibility facade; implementation and color-name data live in nodalia-image-codecs.
use crate::{CodecError, Image, Limits, bridge};
use nodalia_image_codecs::Format;

pub fn x11_color_rgb(name: &str) -> Option<[f32; 3]> {
    nodalia_image_codecs::xpm_named_color_rgb(name)
}
pub fn looks_like_xpm(bytes: &[u8]) -> bool {
    nodalia_image_codecs::detect(bytes) == Some(Format::Xpm)
}
pub fn decode(bytes: &[u8], limits: &Limits) -> Result<Image, CodecError> {
    bridge::format(Format::Xpm, bytes, limits)
}
