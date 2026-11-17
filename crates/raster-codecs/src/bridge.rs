//! Compatibility between this crate's small-format facade and the canonical image codec model.

use crate::{ChannelLayout, CodecError, DecodeWarning, Image, Limits, SampleType};
use nodalia_image_codecs::{DecodeOptions, Format, Metadata};

pub(crate) fn format(format: Format, bytes: &[u8], limits: &Limits) -> Result<Image, CodecError> {
    let shared_limits = nodalia_image_codecs::Limits::new(limits.max_width, limits.max_height, limits.max_pixels, limits.max_alloc);
    let options = DecodeOptions { limits: shared_limits, ..DecodeOptions::default() };
    let image = nodalia_image_codecs::decode_as_with(format, bytes, &options).map_err(from_shared_error)?;
    from_shared_image(image)
}

pub(crate) fn shared_image(image: &Image) -> Result<nodalia_image_codecs::Image, CodecError> {
    let layout = match image.layout() {
        ChannelLayout::Gray => nodalia_image_codecs::ChannelLayout::Gray,
        ChannelLayout::GrayA => nodalia_image_codecs::ChannelLayout::GrayA,
        ChannelLayout::Rgb => nodalia_image_codecs::ChannelLayout::Rgb,
        ChannelLayout::Rgba => nodalia_image_codecs::ChannelLayout::Rgba,
        ChannelLayout::Cmyk => nodalia_image_codecs::ChannelLayout::Cmyk,
        ChannelLayout::CmykA => nodalia_image_codecs::ChannelLayout::CmykA,
    };
    let sample = match image.sample_type() {
        SampleType::U8 => nodalia_image_codecs::SampleType::U8,
        SampleType::U16 => nodalia_image_codecs::SampleType::U16,
        SampleType::F32 => nodalia_image_codecs::SampleType::F32,
    };
    let meta = Metadata { dpi: image.dpi, text: image.text.clone(), ..Metadata::default() };
    nodalia_image_codecs::Image::from_raw(image.width(), image.height(), layout, sample, image.data().to_vec())
        .map(|image| image.with_meta(meta))
        .map_err(from_shared_error)
}

fn from_shared_image(image: nodalia_image_codecs::Image) -> Result<Image, CodecError> {
    let layout = match image.layout() {
        nodalia_image_codecs::ChannelLayout::Gray => ChannelLayout::Gray,
        nodalia_image_codecs::ChannelLayout::GrayA => ChannelLayout::GrayA,
        nodalia_image_codecs::ChannelLayout::Rgb => ChannelLayout::Rgb,
        nodalia_image_codecs::ChannelLayout::Rgba => ChannelLayout::Rgba,
        nodalia_image_codecs::ChannelLayout::Cmyk => ChannelLayout::Cmyk,
        nodalia_image_codecs::ChannelLayout::CmykA => ChannelLayout::CmykA,
        _ => return Err(CodecError::InvalidImage(format!("unsupported small-codec layout {:?}", image.layout()))),
    };
    let sample = match image.sample_type() {
        nodalia_image_codecs::SampleType::U8 => SampleType::U8,
        nodalia_image_codecs::SampleType::U16 => SampleType::U16,
        nodalia_image_codecs::SampleType::F32 => SampleType::F32,
        _ => return Err(CodecError::InvalidImage(format!("unsupported small-codec sample type {:?}", image.sample_type()))),
    };
    let mut out = Image::from_raw(image.width(), image.height(), layout, sample, image.data().to_vec())?;
    out.dpi = image.meta.dpi;
    out.text = image.meta.text;
    out.warnings = image
        .warnings
        .into_iter()
        .filter_map(|warning| match warning {
            nodalia_image_codecs::DecodeWarning::MorePages { total } | nodalia_image_codecs::DecodeWarning::MoreParts { total } => {
                Some(DecodeWarning::MorePages { total })
            }
            _ => None,
        })
        .collect();
    Ok(out)
}

pub(crate) fn from_shared_error(error: nodalia_image_codecs::CodecError) -> CodecError {
    match error {
        nodalia_image_codecs::CodecError::UnknownFormat => CodecError::unsupported("image", "unrecognized image format"),
        nodalia_image_codecs::CodecError::Unsupported { format, reason } => CodecError::unsupported(format.name(), reason),
        nodalia_image_codecs::CodecError::Malformed { format, message } => CodecError::malformed(format.name(), message),
        nodalia_image_codecs::CodecError::LimitExceeded(message) => CodecError::LimitExceeded(message),
        nodalia_image_codecs::CodecError::Encode { format, message } => CodecError::Encode { format: format.name(), message },
        nodalia_image_codecs::CodecError::InvalidImage(message) => CodecError::InvalidImage(message),
    }
}

pub(crate) fn encode(image: &Image, format: Format, options: &nodalia_image_codecs::EncodeOptions) -> Result<Vec<u8>, CodecError> {
    let image = shared_image(image)?;
    nodalia_image_codecs::encode(&image, format, options).map_err(from_shared_error)
}
