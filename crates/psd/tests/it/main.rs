//! The crate's integration tests, linked into one test binary.

mod animation;
mod atn_contract;
mod atn_v12;
mod builder;
mod corpus;
mod corpus_atn;
mod layer_block_order;
mod malformed;
mod merged_recovery;
mod proptests;
mod roundtrip;
mod swatch_malformed;
mod tree;

/// A directory of the real-file corpus (feature `corpus`): under `NODALIA_PSD_CORPUS` when set (a
/// Lienzo checkout's `corpus` directory), else `corpus/` at the workspace root.
#[cfg(feature = "corpus")]
fn corpus_dir(sub: &str) -> std::path::PathBuf {
    let root = std::env::var_os("NODALIA_PSD_CORPUS")
        .map_or_else(|| std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../corpus"), std::path::PathBuf::from);
    root.join(sub)
}
