# nodalia-i18n roadmap

> **Last updated:** 2026-11-08 · **Change:** minor (3b: Lienzo cutover started)

Shared translations for the storytold Crafting Apps: one catalog per locale for shared strings,
one per app, checked in CI and embedded by each app at build time. Vocabulary is in
[`GLOSSARY.md`](GLOSSARY.md); decisions are in [`docs/adr/`](docs/adr/).

## Milestones

| # | Milestone | Where | Status |
|---|---|---|---|
| 1 | TSV catalog format and strict checker; Fluent and the unusable library crate removed; translator and integration docs | this repo | done (PR #1) |
| 2 | `nodalia-i18n` runtime crate: parser, lookup, fallback, plurals (`intl_pluralrules`, `icu_plurals` since nodalia-libs#210), locale matching, pseudo locale | nodalia-libs | done: merged upstream as [storytold/craft-libs#167](https://github.com/storytold/craft-libs/pull/167) (2026-10-18) |
| 3a | Migrate Letra and Papel (proves the runtime on the largest catalogs; seeds the shared catalog) | apps | Letra cut over (2026-10-24); Papel synced at `pdfcraft@ecdd1e6`, wiring in progress |
| 3b | Migrate the other TSV apps: Lienzo, Pluma, Toma, Forja, craft-launcher | apps | catalogs moved here (shared catalog grows additively, [ADR 0003](docs/adr/0003-shared-catalog-grows-additively.md)); Forja resynced at `cadcraft@c4d9e6a`; Lienzo synced at `photocraft@2772ac1` (cutover started, 2026-11-08); app wiring next for the rest |
| 3c | Convert and migrate Trama (TOML), Luz (JSON), Pliego, Celdas, Pulso (Rust tables) | apps | not started |
| 3d | Add translation to Lámina and SoundCraft | apps | not started |
| 4 | Language data: spelling dictionaries, hyphenation patterns and the suite word list; English embedded, other languages pinned and downloaded ([ADR 0004](docs/adr/0004-third-party-language-data.md), [ADR 0005](docs/adr/0005-language-data-lives-here.md)) | this repo, nodalia-libs, apps | licence table signed off 2026-11-01 (Martin Ball); phase 1 done; phase 2 (SCOWL 2026 en-US/en-GB/en-CA/en-AU dictionaries) added; phase 3 (pack manifest, checks, release workflow) done; phase 3 follow-up (75 of 80 locales publishable, 2 hidden, 3 Excluded); the last 14 need craft-proof at `47c9f625` (nodalia-libs #497 merged) |

Each app migration: confirm the app is MIT OR Apache-2.0, move its catalogs here (lowercase BCP 47
names, origin recorded in `ATTRIBUTION.md`), add the `build.rs` recipe from
[`docs/integration.md`](docs/integration.md), switch to the runtime crate, delete the app's copied
i18n module, and add the app-side stale/missing string report.

Known migration fixes: Papel's Turkish `@plural` rows listed one form, CLDR (and CI) need two;
done in 3a by repeating the form (Turkish nouns stay singular after numerals). Papel's Hindi
`@plural` rows (14, added after 3a) also listed one form; the cutover sync repeated it, so Hindi
shows what it does today. The checker takes each locale's plural form count from the runtime crate
itself (a dependency pinned by git rev; the crate's own CLDR 48.2.1 data, on `icu_plurals` since
storytold/craft-libs#210), so the two can't disagree; `tests/runtime_agreement.rs` also feeds the
crate every catalog's `@plural` rows.

Done in 3b, format only (no wording changes): Hungarian and Turkish `@plural` rows with one form
got it repeated (Lienzo, Pluma); Pluma's Korean and Forja's Chinese kept one
form; Forja's `\P` is escaped as `\\P`. Forja's `@plural` sources were the singular only;
they are now `one|other`, so **Forja's `count()` must look plurals up by `one|other`** when it
is wired. Lienzo's `sr` catalog is Latin script and moved to `sr-latn`.

Known homograph, not yet fixed: Letra's Paragraph Spacing menu has an "Open" preset
(`crates/ui-egui/src/ribbon.rs`, the spacing next to Tight and Relaxed). It shares the key
`("", "Open")` with File > Open, so every locale shows the verb (`es` Abrir, `de` Öffnen). The fix is
app-side in Letra's 3a wiring: give the preset a context (`spacing`) and add rows with context `spacing` to
`letra.tsv`. Found by FredApps/craftlingo#1.

## Related work

aiongg's language-support plan, [storytold/craft-libs#198](https://github.com/storytold/craft-libs/issues/198)
(fonts in [#197](https://github.com/storytold/craft-libs/issues/197)), extends the runtime crate
(scripts, isolation, number formatting, file sizes, sorting) and lists moving the apps onto
nodalia-i18n as this roadmap's milestones 3a–3d. Its pilots delete Papel's and Forja's own
Arabic reordering; each of the two is wired once it draws catalogs in logical order on the patched
egui. Papel got there first (2026-11-03, storytold/egui 6d518fc) and is wired now; Forja still waits.

Known clash for 3c: aiongg's Pliego pilot rewrites the app's 1,010 right-to-left call sites,
and 3c converts Pliego's Rust tables. The order is decided when 3c starts.

## Apps

As surveyed on 2026-10-16 (Pluma recounted 2026-10-18). Locale counts exclude English.

| App | Format today | Locales | Plurals | Migrated |
|---|---|---|---|---|
| Letra | TSV | 22 | none | catalogs |
| Papel | TSV | 22 | `@plural` | catalogs |
| Lienzo | TSV | 20 | `@plural` | catalogs |
| Pluma | TSV | 22 | `@plural` | catalogs |
| Toma | TSV | 11 | none | catalogs |
| Forja | TSV | 12 | `@plural` + own rules | catalogs |
| craft-launcher | TSV | 10 | `@plural` | catalogs |
| Trama | TOML | 14 | CLDR | no |
| Luz | JSON | 13 | minimal | no |
| Pliego | Rust tables | 11 | own rules | no |
| Celdas | Rust `match` | 9 | none | no |
| Pulso | Rust tables | 10 | none | no |
| Lámina | none | 0 | – | no |
| SoundCraft | none | 0 | – | no |

## Open decisions

- **Release builds** (maintainer): whether craft-common-actions' release workflow checks out
  nodalia-i18n at a pinned ref and sets `NODALIA_I18N_DIR` and `NODALIA_I18N_REQUIRED=1`, as it does for
  nodalia-fonts. Until then, releases are English-only unless an app sets them itself.
- **Repository home**: transferred to getnodalia/foundation (nodalia/i18n) (2026-10-21).

## Change log

| Date | Change | Summary |
|---|---|---|
| 2026-10-16 | major | First roadmap: milestones 1–3d, per-app survey, open decisions |
| 2026-10-17 | minor | Milestones 1 and 2 done; Letra and Papel catalogs migrated (196 shared strings, 28 locales) |
| 2026-10-17 | patch | Milestone 2 runtime crate opened upstream as storytold/craft-libs#167 |
| 2026-10-18 | patch | Recorded Letra's "Open" spacing preset translated as the verb |
| 2026-10-18 | minor | Milestone 3b catalogs migrated: Lienzo, Pluma, Toma, Forja, craft-launcher (1279 shared strings, 32 locales) |
| 2026-10-18 | patch | Milestone 2 done: storytold/craft-libs#167 merged after review; app wiring unblocked |
| 2026-10-22 | patch | Repository transferred to getnodalia/foundation (nodalia/i18n) |
| 2026-10-22 | minor | Related work: storytold/craft-libs#198; Papel and Forja wired last; plural engine follow-up; Pliego clash noted for 3c |
| 2026-11-01 | minor | Milestone 4 phase 3: Language pack manifest (80 locales), checks, load-and-check per pack with craft-proof, release workflow (`docs/language-data-format.md`) |
| 2026-11-01 | patch | ADR 0004 licence table signed off (Martin Ball, 2026-11-01): the LGPL/MPL/LPPL/GPL switch is retired; uk Excluded pending its NC source data |
| 2026-11-01 | minor | Milestone 4 phase 2: SCOWL `rel-2026.02.25` Hunspell dictionaries for en-US, en-GB (-ise), en-CA and en-AU in `language-data/`, unmodified, with their licence notices |
| 2026-11-01 | patch | `en-variants.txt`: `judgment`/`judgement` (and `-al`) right in every English, now that each English checks only its own SCOWL dictionary (nodalia-libs#483 review) |
| 2026-11-01 | minor | Milestone 4 phase 3 follow-up: ar, be, ca, ca-valencia, cy, el, fr, he, hy, id, is, ka, lv, mk, sk, sr, sr-latn, tr, af, ko, gl unhidden (61 published, 16 hidden, 3 Excluded); hidden reasons name the current compounding gaps; gl check word fixed (gl now published); Moby `en-us.dic` loses typos teh, abd, nad, ur, u, r; licence file names checked as the consumer does; craft-proof dev-dependency pinned at getnodalia/foundation (nodalia/libs) `8f16fe5a` (the restacked #485 stack top), still valid once #482–#490 merge with merge commits |
| 2026-11-02 | minor | Milestone 4 phase 3, compounding: da, de, de-at, de-ch, eo, et, fa, hr, hu, nb, nl, nn, sv, sv-fi unhidden (75 published, 2 hidden, 3 Excluded; mn stays hidden: suggestions take 200–580 ms over its 12,066 affix rules; th stays hidden: craft-proof splits words only at spaces and punctuation, so a Thai sentence would be checked as one word); needs craft-proof flag-based compounding (nodalia-libs #497, merged at `47c9f625`); de, de-at, de-ch check words now capitalised nouns and et, nb, nn have real misspellings, each checked with the hunspell 1.7.5 CLI; nb and nn hyphenate with hyph-no.tex (their own files hold only exceptions) |
| 2026-11-03 | minor | 3a: Papel cutover sync (`pdfcraft@ecdd1e6`, 12 new Papel locales); Papel wired now, not last: it already draws logical catalogs on storytold/egui |
| 2026-11-03 | patch | Checker takes each locale's plural form count from the runtime crate (`nodalia-i18n` at getnodalia/foundation (nodalia/libs) `32b2fd8a`, a normal dependency; its own CLDR 48.2.1 data on `icu_plurals` since nodalia-libs#210), replacing `intl_pluralrules` 7.0.2 and its Hebrew workaround; `icu_plurals`' compiled data has no `ckb` rules (1 form), the crate's data has 2; `tests/runtime_agreement.rs` checks every locale's count and that the crate accepts every catalog's `@plural` rows; no existing locale's count changed |
| 2026-11-03 | minor | File sizes (storytold/craft-libs#204): `@plural {n} byte\|{n} bytes` moved from 20 locales' `papel.tsv` to `common.tsv` (additive, ADR 0003); `unit` rows (`{n} KB`, `{n} MiB`, …) only where the symbol differs from English: `fr`, `ru`, `uk` |
| 2026-11-05 | minor | Forja resync before its cutover (`cadcraft@b23d362` → `cadcraft@c4d9e6a`): its Greek, Hungarian, Turkish and Vietnamese catalogs (added in the app after the 3b migration) are new here; every other Forja catalog takes the app's added and corrected rows and drops the prompt texts the app reworded |
| 2026-11-08 | minor | 3b: Lienzo cutover sync (`photocraft@8d2e615` → `photocraft@70c0911`, 12 new Lienzo locales: ar, az, da, fi, he, hi, nb, ro, sv, ta, th, ur; `az` is new to nodalia-i18n); Hebrew's 35 `@plural` rows repeat the `other` form for CLDR's third form; credits follow Lienzo's `LICENSE-translations.txt` |
