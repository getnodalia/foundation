# Lookup code lives in nodalia-libs; nodalia-i18n holds only data

The catalog parser, lookup, plural rules (`intl_pluralrules`), locale matching and pseudo locale
live in a `nodalia-i18n` crate in nodalia-libs. This repository holds only catalogs, docs and the CI
that checks them. Apps embed the catalogs at build time from `NODALIA_I18N_DIR`, as they do with
nodalia-fonts, and never list this repository in `Cargo.toml`.

Each app had its own copy of the i18n module, and the copies drifted (Letra's and Papel's
`mod.rs` differ by ~3.4k lines). Apps already depend on nodalia-libs as a pinned git dependency, so
the code there costs no new dependency. The data stays optional: a build without
`NODALIA_I18N_DIR` is English-only but still builds offline, in a fork or on a mirror.

## Considered options

- **Code per app** (status quo): rejected, it is what drifted.
- **Code in this repository as a git dependency**: rejected, it adds a second git dependency and
  makes the data repository mandatory for every build.

## Amendment: Language data (2026-11-01)

[ADR 0005](0005-language-data-lives-here.md) adds Language data (spelling dictionaries,
hyphenation patterns, the suite word list) to the data held here. The split is unchanged: data
here, code in nodalia-libs, and a build without `NODALIA_I18N_DIR` still builds offline.
