# Nodalia brand

The identity of Nodalia as a whole: the mark, the wordmark, the colours and type that go with
them, the website icons and the application icons. Every app, the website, Nodalix OS and every
release page take their Nodalia identity from here. The visual language of the interfaces
themselves is not here: that is [Nodalia Design](https://github.com/getnodalia/nodalia-design).

All files are original work for Nodalia, published under `MIT OR Apache-2.0` like the rest of this
repository, except the fonts, which keep their own licence (see below). Nobody else's artwork is
in this directory.

## Files

| File | Use |
|---|---|
| `nodalia-mark.svg` | The mark on its dark rounded tile. The default square logo: avatars, favicons, app stores, social cards. |
| `nodalia-mark-bare.svg` | The mark alone, light, for dark backgrounds. |
| `nodalia-mark-bare-dark.svg` | The mark alone, dark, for light backgrounds. |
| `nodalia-wordmark-light.svg` | Mark plus the name `nodalia`, light, for dark backgrounds. |
| `nodalia-wordmark-dark.svg` | Mark plus the name, dark, for light backgrounds. |
| `nodalia-placa-preview.png` | The wordmark on its plate, on light and on dark, 1440 × 300. A preview and a reference for the plate, not a master. |
| `web/` | `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, as the website serves them. |
| `app-icons/` | The application icons at 192 px as the website shows them. The masters live in `nodalia-design` (`packages/icons`) and `nodalix-icon-theme`. |
| `fonts/` | The licences of the two brand typefaces. The font files themselves live in `nodalia-design` (`packages/fonts`). |

## The mark

An `n` built from one bar and one arch, with a small square at its foot, the node, filled with the
only gradient the brand uses. It is drawn on a 64 × 64 grid; the bare mark occupies `8 8 48 48`.

## Colour

| Role | Value |
|---|---|
| Ink (tile, text on light) | `#0B0D13` |
| Paper (mark and text on dark) | `#F4F5F9` |
| Node gradient, start | `#8ADBE0` |
| Node gradient, end | `#A79BFF` |

The gradient exists only inside the node square of the mark. Nothing else in the identity uses a
gradient or a glow. Interface colours (surfaces, text, status) come from the NDL tokens; each app
adds a single accent, listed in NDL's `packages/tokens/src/accents.json`.

## Type

`Sora` for titles and `Inter` for text, both SIL Open Font License 1.1 (`fonts/OFL-*.txt`).
Interfaces fall back to the system stack when they are not installed.

## Using it

- Light mark and wordmark on dark, dark ones on light. Do not recolour them, outline them, add
  shadows or effects, rotate, stretch or redraw them.
- Leave clear space around a logo of at least the height of the node square, and do not show the
  mark smaller than 16 px or the wordmark smaller than 80 px wide.
- The wordmark is lower case: `nodalia`.
- An app's own icon is its own and follows the portrait rule below; the Nodalia mark never
  replaces it and is never put inside it.

## Application icons

Every Nodalia app icon is a portrait of a historical figure related to what the app does, for
example Maudslay for Torno, Méliès for Toma, Jacquard for Trama, Reynaud for Ánima, Gutenberg for
Pliego and Aldus Manutius for Papel. The icons are original illustrations made for Nodalia. A new
app gets its own figure; the list and the generator are in `nodalia-design`.

The Nodalix OS icon theme (`nodalix-icon-theme`) keeps the icons of third-party applications as
they are; only Nodalia's own apps use the portraits.

## Changing this directory

Brand changes are decided by Daniel. A change here comes with the same change in
`nodalia-web/assets` (the website's copy) in the same week, so the two do not drift.
