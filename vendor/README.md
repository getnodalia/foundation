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

## Depending on it

Cargo finds a package by name anywhere in the commit it checks out, so the dependency keeps its
`rev` and only the URL changes:

```toml
craft-color = { git = "https://github.com/getnodalia/foundation", rev = "1b34eba41e62138fc2438d2734523b302840b45d" }
```

In `Cargo.lock` the source becomes `git+https://github.com/getnodalia/foundation?rev=<sha>#<sha>`
with the same SHA. Build inputs are checked out by commit the same way:

```yaml
- uses: actions/checkout@<sha> # v7.0.1
  with:
    repository: getnodalia/foundation
    ref: b076417b5880bd4154bd22f00695b1d28c6bea83 # craft-fonts
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
