//! The craft libraries in one dependency. Turn on one feature per crate and `ui` for their
//! egui side; import through `craft::<crate>`.
#![warn(missing_docs)]

pub mod egui_fork;

#[cfg(all(feature = "ui-system_fonts", target_arch = "wasm32"))]
compile_error!("`ui-system_fonts` is desktop-only: the system font index needs fontique, which has no web build");
#[cfg(feature = "aaf")]
pub use nodalia_aaf as aaf;
#[cfg(feature = "aep")]
pub use nodalia_aep as aep;
#[cfg(feature = "affinity")]
pub use nodalia_affinity as affinity;
#[cfg(feature = "ai")]
pub use nodalia_ai as ai;
#[cfg(feature = "ai-core")]
pub use nodalia_ai_core as ai_core;
#[cfg(feature = "anima-format")]
pub use nodalia_anima_format as anicraft_format;
#[cfg(feature = "assuan")]
pub use nodalia_assuan as assuan;
#[cfg(feature = "atomic")]
pub use nodalia_atomic as atomic;
#[cfg(feature = "audio")]
pub use nodalia_audio as audio;
#[cfg(feature = "automation")]
pub use nodalia_automation as automation;
pub use nodalia_behavior as behavior;
#[cfg(feature = "ber")]
pub use nodalia_ber as ber;
#[cfg(feature = "browse")]
pub use nodalia_browse as browse;
#[cfg(feature = "captions")]
pub use nodalia_captions as captions;
#[cfg(feature = "cfb")]
pub use nodalia_cfb as cfb;
#[cfg(feature = "cloud")]
pub use nodalia_cloud as cloud;
#[cfg(feature = "cloud-local")]
pub use nodalia_cloud_local as cloud_local;
#[cfg(feature = "cloud-ui")]
pub use nodalia_cloud_ui as cloud_ui;
#[cfg(feature = "cms")]
pub use nodalia_cms as cms;
#[cfg(feature = "codepage")]
pub use nodalia_codepage as codepage;
#[cfg(feature = "color")]
pub use nodalia_color as color;
#[cfg(feature = "color-ui")]
pub use nodalia_color_ui as color_ui;
#[cfg(feature = "control")]
pub use nodalia_control as control;
#[cfg(feature = "control-protocol")]
pub use nodalia_control_protocol as control_protocol;
#[cfg(feature = "crs")]
pub use nodalia_crs as crs;
#[cfg(feature = "crw")]
pub use nodalia_crw as crw;
#[cfg(feature = "csv")]
pub use nodalia_csv as csv;
#[cfg(feature = "dav")]
pub use nodalia_dav as dav;
#[cfg(feature = "dds")]
pub use nodalia_dds as dds;
#[cfg(feature = "lamina-format")]
pub use nodalia_lamina_format as deckcraft_format;
#[cfg(feature = "pliego-format")]
pub use nodalia_pliego_format as designcraft_format;
#[cfg(feature = "dialogs")]
pub use nodalia_dialogs as dialogs;
#[cfg(feature = "doc")]
pub use nodalia_doc as doc;
#[cfg(feature = "doc-binary")]
pub use nodalia_doc_binary as doc_binary;
#[cfg(feature = "docpath")]
pub use nodalia_docpath as docpath;
#[cfg(feature = "document-bundle")]
pub use nodalia_document_bundle as document_bundle;
#[cfg(feature = "docx")]
pub use nodalia_docx as docx;
#[cfg(feature = "dpx")]
pub use nodalia_dpx as dpx;
#[cfg(feature = "draw")]
pub use nodalia_draw as draw;
#[cfg(feature = "drawingml")]
pub use nodalia_drawingml as drawingml;
#[cfg(feature = "dwg")]
pub use nodalia_dwg as dwg;
#[cfg(feature = "dxf")]
pub use nodalia_dxf as dxf;
#[cfg(feature = "ecproj-format")]
pub use nodalia_ecproj_format as ecproj_format;
#[cfg(feature = "elf")]
pub use nodalia_elf as elf;
#[cfg(feature = "eps")]
pub use nodalia_eps as eps;
#[cfg(feature = "epub")]
pub use nodalia_epub as epub;
#[cfg(feature = "ews")]
pub use nodalia_ews as ews;
#[cfg(feature = "exr")]
pub use nodalia_exr as exr;
#[cfg(feature = "fcproj-format")]
pub use nodalia_fcproj_format as fcproj_format;
#[cfg(feature = "fig")]
pub use nodalia_fig as fig;
#[cfg(feature = "trama-format")]
pub use nodalia_trama_format as figcraft_format;
#[cfg(feature = "figma-rest")]
pub use nodalia_figma_rest as figma_rest;
#[cfg(feature = "file-formats")]
pub use nodalia_file_formats as file_formats;
#[cfg(feature = "file-import")]
pub use nodalia_file_import as file_import;
#[cfg(feature = "flags")]
pub use nodalia_flags as flags;
#[cfg(feature = "flow")]
pub use nodalia_flow as flow;
#[cfg(feature = "font-catalog")]
pub use nodalia_font_catalog as font_catalog;
#[cfg(feature = "font-manager")]
pub use nodalia_font_manager as font_manager;
#[cfg(feature = "font-store")]
pub use nodalia_font_store as font_store;
#[cfg(feature = "font-subset")]
pub use nodalia_font_subset as font_subset;
#[cfg(feature = "format")]
pub use nodalia_format as format;
#[cfg(feature = "frame")]
pub use nodalia_frame as frame;
#[cfg(feature = "gainmap")]
pub use nodalia_gainmap as gainmap;
#[cfg(feature = "gcode")]
pub use nodalia_gcode as gcode;
#[cfg(feature = "gif")]
pub use nodalia_gif as gif;
#[cfg(feature = "celdas-format")]
pub use nodalia_celdas_format as gridcraft_format;
#[cfg(feature = "gzip")]
pub use nodalia_gzip as gzip;
#[cfg(feature = "har")]
pub use nodalia_har as har;
#[cfg(feature = "hdr")]
pub use nodalia_hdr as hdr;
#[cfg(feature = "heif")]
pub use nodalia_heif as heif;
pub use nodalia_host as host;
#[cfg(feature = "html")]
pub use nodalia_html as html;
#[cfg(feature = "http-url")]
pub use nodalia_http_url as http_url;
pub use nodalia_i18n as i18n;
#[cfg(feature = "ical")]
pub use nodalia_ical as ical;
#[cfg(feature = "idml")]
pub use nodalia_idml as idml;
#[cfg(feature = "image-codecs")]
pub use nodalia_image_codecs as image_codecs;
#[cfg(feature = "imaging")]
pub use nodalia_imaging as imaging;
#[cfg(feature = "indd")]
pub use nodalia_indd as indd;
#[cfg(feature = "ipc")]
pub use nodalia_ipc as ipc;
#[cfg(feature = "java-class")]
pub use nodalia_java_class as java_class;
#[cfg(feature = "jmap")]
pub use nodalia_jmap as jmap;
#[cfg(feature = "jpeg")]
pub use nodalia_jpeg as jpeg;
#[cfg(feature = "jsonc")]
pub use nodalia_jsonc as jsonc;
#[cfg(feature = "jsonrpc")]
pub use nodalia_jsonrpc as jsonrpc;
#[cfg(feature = "jxl")]
pub use nodalia_jxl as jxl;
#[cfg(feature = "keymap")]
pub use nodalia_keymap as keymap;
#[cfg(feature = "kiwi")]
pub use nodalia_kiwi as kiwi;
#[cfg(feature = "kra")]
pub use nodalia_kra as kra;
#[cfg(feature = "latex")]
pub use nodalia_latex as latex;
#[cfg(feature = "layers")]
pub use nodalia_layers as layers;
#[cfg(feature = "lottie")]
pub use nodalia_lottie as lottie;
#[cfg(feature = "macho")]
pub use nodalia_macho as macho;
#[cfg(feature = "markdown")]
pub use nodalia_markdown as markdown;
#[cfg(feature = "materialx")]
pub use nodalia_materialx as materialx;
#[cfg(feature = "math")]
pub use nodalia_math as math;
#[cfg(feature = "mcmat")]
pub use nodalia_mcmat as mcmat;
#[cfg(feature = "mcp")]
pub use nodalia_mcp as mcp;
#[cfg(feature = "mcp-server")]
pub use nodalia_mcp_server as mcp_server;
#[cfg(feature = "media")]
pub use nodalia_media as media;
#[cfg(feature = "media-source")]
pub use nodalia_media_source as media_source;
#[cfg(feature = "menu")]
pub use nodalia_menu as menu;
#[cfg(feature = "mesh")]
pub use nodalia_mesh as mesh;
#[cfg(feature = "metadata")]
pub use nodalia_metadata as metadata;
#[cfg(feature = "metafile")]
pub use nodalia_metafile as metafile;
#[cfg(feature = "midi")]
pub use nodalia_midi as midi;
#[cfg(feature = "mime")]
pub use nodalia_mime as mime;
#[cfg(feature = "odf")]
pub use nodalia_odf as odf;
#[cfg(feature = "ods")]
pub use nodalia_ods as ods;
#[cfg(feature = "offcrypto")]
pub use nodalia_offcrypto as offcrypto;
#[cfg(feature = "opc")]
pub use nodalia_opc as opc;
#[cfg(feature = "openpgp")]
pub use nodalia_openpgp as openpgp;
#[cfg(feature = "ora")]
pub use nodalia_ora as ora;
#[cfg(feature = "pages")]
pub use nodalia_pages as pages;
#[cfg(feature = "palette")]
pub use nodalia_palette as palette;
#[cfg(feature = "pcap")]
pub use nodalia_pcap as pcap;
#[cfg(feature = "lienzo-bundle")]
pub use nodalia_lienzo_bundle as pcraft_bundle;
#[cfg(feature = "lienzo-format")]
pub use nodalia_lienzo_format as pcraft_format;
#[cfg(feature = "pdf")]
pub use nodalia_pdf as pdf;
#[cfg(feature = "pdn")]
pub use nodalia_pdn as pdn;
#[cfg(feature = "pe")]
pub use nodalia_pe as pe;
#[cfg(feature = "penpot")]
pub use nodalia_penpot as penpot;
#[cfg(feature = "pkcs7")]
pub use nodalia_pkcs7 as pkcs7;
#[cfg(feature = "platform")]
pub use nodalia_platform as platform;
#[cfg(feature = "plist")]
pub use nodalia_plist as plist;
#[cfg(feature = "plotter")]
pub use nodalia_plotter as plotter;
#[cfg(feature = "pptx")]
pub use nodalia_pptx as pptx;
#[cfg(feature = "prc")]
pub use nodalia_prc as prc;
#[cfg(feature = "prepress")]
pub use nodalia_prepress as prepress;
#[cfg(feature = "press-print")]
pub use nodalia_press_print as press_print;
#[cfg(feature = "print")]
pub use nodalia_print as print;
#[cfg(feature = "proof")]
pub use nodalia_proof as proof;
#[cfg(feature = "proto")]
pub use nodalia_proto as proto;
#[cfg(feature = "ps")]
pub use nodalia_ps as ps;
#[cfg(feature = "psd")]
pub use nodalia_psd as psd;
#[cfg(feature = "pst")]
pub use nodalia_pst as pst;
#[cfg(feature = "quit")]
pub use nodalia_quit as quit;
#[cfg(feature = "raster-codecs")]
pub use nodalia_raster_codecs as raster_codecs;
#[cfg(feature = "raw")]
pub use nodalia_raw as raw;
#[cfg(feature = "review")]
pub use nodalia_review as review;
#[cfg(feature = "rtf")]
pub use nodalia_rtf as rtf;
#[cfg(feature = "score")]
pub use nodalia_score as score;
#[cfg(feature = "sound-format")]
pub use nodalia_sound_format as scraft_format;
#[cfg(feature = "settings")]
pub use nodalia_settings as settings;
#[cfg(feature = "sf2")]
pub use nodalia_sf2 as sf2;
#[cfg(feature = "sheet")]
pub use nodalia_sheet as sheet;
#[cfg(feature = "shx")]
pub use nodalia_shx as shx;
#[cfg(feature = "silhouette-studio")]
pub use nodalia_silhouette_studio as silhouette_studio;
#[cfg(feature = "sketch")]
pub use nodalia_sketch as sketch;
#[cfg(feature = "smime")]
pub use nodalia_smime as smime;
#[cfg(feature = "sniff")]
pub use nodalia_sniff as sniff;
#[cfg(feature = "sourcemap")]
pub use nodalia_sourcemap as sourcemap;
#[cfg(feature = "ssip")]
pub use nodalia_ssip as ssip;
#[cfg(feature = "stencil-document")]
pub use nodalia_stencil_document as stencilcraft_document;
#[cfg(feature = "stencil-format")]
pub use nodalia_stencil_format as stencilcraft_format;
#[cfg(feature = "stream-codecs")]
pub use nodalia_stream_codecs as stream_codecs;
#[cfg(feature = "svg")]
pub use nodalia_svg as svg;
#[cfg(feature = "table")]
pub use nodalia_table as table;
#[cfg(feature = "tar")]
pub use nodalia_tar as tar;
#[cfg(feature = "texture-archive")]
pub use nodalia_texture_archive as tcraft;
#[cfg(feature = "text")]
pub use nodalia_text as text;
#[cfg(feature = "texture")]
pub use nodalia_texture as texture;
#[cfg(feature = "tga")]
pub use nodalia_tga as tga;
pub use nodalia_theme as theme;
#[cfg(feature = "theme-editor")]
pub use nodalia_theme_editor as theme_editor;
#[cfg(feature = "theme-store")]
pub use nodalia_theme_store as theme_store;
#[cfg(feature = "tiff")]
pub use nodalia_tiff as tiff;
#[cfg(feature = "time")]
pub use nodalia_time as time;
#[cfg(feature = "timeline")]
pub use nodalia_timeline as timeline;
#[cfg(feature = "ui")]
pub use nodalia_ui as ui;
#[cfg(feature = "update")]
pub use nodalia_update as update;
#[cfg(feature = "usd")]
pub use nodalia_usd as usd;
#[cfg(feature = "vcard")]
pub use nodalia_vcard as vcard;
#[cfg(feature = "pluma-format")]
pub use nodalia_pluma_format as vectorcraft_format;
#[cfg(feature = "vectordrawable")]
pub use nodalia_vectordrawable as vectordrawable;
#[cfg(feature = "video")]
pub use nodalia_video as video;
#[cfg(feature = "wasm")]
pub use nodalia_wasm as wasm;
#[cfg(feature = "web-api")]
pub use nodalia_web_api as web_api;
#[cfg(feature = "web-host")]
pub use nodalia_web_host as web_host;
#[cfg(feature = "webp")]
pub use nodalia_webp as webp;
#[cfg(feature = "window")]
pub use nodalia_window as window;
#[cfg(feature = "wordmodel")]
pub use nodalia_wordmodel as wordmodel;
#[cfg(feature = "xcf")]
pub use nodalia_xcf as xcf;
#[cfg(feature = "xfdf")]
pub use nodalia_xfdf as xfdf;
#[cfg(feature = "xfl")]
pub use nodalia_xfl as xfl;
#[cfg(feature = "xls")]
pub use nodalia_xls as xls;
#[cfg(feature = "xlsx")]
pub use nodalia_xlsx as xlsx;
#[cfg(feature = "xml")]
pub use nodalia_xml as xml;
#[cfg(feature = "y4m")]
pub use nodalia_y4m as y4m;
#[cfg(feature = "zip")]
pub use nodalia_zip as zip;
#[cfg(feature = "ui")]
pub use egui;

/// The types an app imports first: the host handle, a dialog stack, the dialog outcome and the theme
/// tokens.
pub mod prelude {
    pub use nodalia_host::{AppInfo, Host, Section};
    pub use nodalia_theme::Tokens;
    #[cfg(feature = "ui")]
    pub use nodalia_ui::{contract::Outcome, dialog::DialogStack};
}

#[cfg(test)]
extern crate self as craft;

#[cfg(test)]
#[path = "../tests/main.rs"]
mod integration;
