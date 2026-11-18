# Vendored code

Nodalia apps build against libraries and build inputs that came from `storytold`. They now live in
this repository, so no Nodalia build depends on another organization being online. Each one is
kept **with its full history** on its own branches, `vendor/<repo>/<upstream-branch>`, so every
commit keeps the SHA the apps already pin: moving an app here changes the URL and nothing else.

Nothing here was rewritten. Each branch carries the upstream tree as it was, with its own
`LICENSE*`, `NOTICE` and `ATTRIBUTION` files; those files are the authority on licensing, and this
table only summarises them.

| Code | Branches here | Upstream | Licence | Used by |
|---|---|---|---|---|
| craft-libs | `vendor/craft-libs/main`, `vendor/craft-libs/pin-787a7a0` | storytold/craft-libs | MIT OR Apache-2.0 (+ `NOTICE`, `licenses/`) | the Rust desktop apps |
| egui | `vendor/egui/main`, `vendor/egui/craft-0.36.2`, `vendor/egui/migration-egui-037-20261024` | storytold/egui (from emilk/egui) | MIT OR Apache-2.0 | the Rust desktop apps |
| winit | `vendor/winit/master`, `vendor/winit/craft-0.30.13` | storytold/winit (from rust-windowing/winit) | Apache-2.0 | the Rust desktop apps |
| winprint.rs | `vendor/winprint.rs/main` | storytold/winprint.rs | BSD-3-Clause, © alampy.com | Windows printing |
| indd-utils | `vendor/indd-utils/main` | storytold/indd-utils | MIT OR Apache-2.0 | Pliego |
| filmcraft | `vendor/filmcraft/main` | storytold/filmcraft | MIT OR Apache-2.0 (+ `NOTICE`) | Pulso |
| craft-fonts | `vendor/craft-fonts/main` | storytold/craft-fonts | repository MIT OR Apache-2.0; each font under its own licence (see its `ATTRIBUTION.md`) | font build input |
| craft-i18n | `vendor/craft-i18n/main` | storytold/craft-i18n | MIT OR Apache-2.0; translators credited in its `ATTRIBUTION.md` | translations build input |

`pin-787a7a0`, `craft-0.36.2`, `craft-0.30.13` and `migration-egui-037-20261024` exist because an
app pins a commit that upstream only kept on that branch (or, for `787a7a0`, only on a pull
request). Without the branch the commit would not be reachable here.

`storytold/craft-common-actions` is **not** here: it has no licence, so Nodalia's workflows in
`.github/workflows/` were written from scratch.

## Nodalia names

Apps never depend on a mirror directly: they depend on the same code under Nodalia's names,
which `scripts/nodalia_libs.py` makes from the mirrors and the **Nodalia libraries** workflow
publishes on four branches of its own:

| Branch | Made from | What changes |
|---|---|---|
| `nodalia/libs` | `vendor/craft-libs/*` | every `craft-*` crate is `nodalia-*` (`craft_ui` is `nodalia_ui`); crates named after an upstream app take the Nodalia app's name (`craft-pcraft-format` is `nodalia-lienzo-format`); `CRAFT_*` variables are `NODALIA_*` |
| `nodalia/i18n` | `vendor/craft-i18n/*` | the same, and each app's catalog has the app's name (`pdfcraft.tsv` is `papel.tsv`, `wordcraft.tsv` is `letra.tsv`) |
| `nodalia/fonts` | `vendor/craft-fonts/*` | the same (`NODALIA_FONTS_DIR`) |
| `nodalia/winprint` | `vendor/winprint.rs/*` | the GDI helper crate is `nodalia-winprint-gdi` |

What never changes: licence texts, `NOTICE` (it gains a paragraph saying where the tree comes
from), `ATTRIBUTION.md`, third-party code under `vendor/`, links and credits, and the lower-case
product words that are file signatures, so documents saved before keep opening.

Each generated commit has two parents: the previous generated commit and the upstream commit it
was made from, so the full history and its authors stay reachable. Its message ends with
`Upstream-Commit: <sha>`. `nodalia_libs.py lookup libs <upstream sha>` prints the matching
commit; an app moves to it, and its weekly upstream sync keeps it there, with
`nodalia_libs.py app <checkout> --repo <foundation clone>`, which renames the app's uses and
maps every pinned SHA. The workflow runs when a `vendor/` branch moves, every Monday before the
apps' syncs, and on request for a commit an app needs (`library` and `commits` inputs).

Translations, fonts and fixes still go to the `vendor/` branches by pull request; the generated
branches are never edited by hand.

## Depending on it

Cargo finds a package by name anywhere in the commit it checks out, so the dependency keeps its
`rev` and only the URL changes:

```toml
nodalia-color = { git = "https://github.com/getnodalia/foundation", rev = "<nodalia/libs commit>" }
```

In `Cargo.lock` the source becomes `git+https://github.com/getnodalia/foundation?rev=<sha>#<sha>`
with the same SHA. Build inputs are checked out by commit the same way:

```yaml
- uses: actions/checkout@<sha> # v7.0.1
  with:
    repository: getnodalia/foundation
    ref: <nodalia/fonts commit> # nodalia-fonts
    path: .nodalia/fonts
    persist-credentials: false
```

## Changing it

A change is a pull request against the `vendor/...` branch, reviewed like any other code. Pulling
from an upstream that still exists is a deliberate merge into that branch, never an automatic sync.
The commits apps pin must stay reachable: never force-push or delete a `vendor/` branch.

Imported 2026-11-12. Upstream heads at import: craft-libs `f92a91a`, egui `faa2876`, winit
`7f66c99`, winprint.rs `e90c444`, indd-utils `136f973`, filmcraft `cb9783b`, craft-fonts `c1db6d1`,
craft-i18n `74e7770`.
