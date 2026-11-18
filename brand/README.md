# Nodalia brand

Everything that makes Nodalia look like Nodalia, in one place: the logo and wordmarks, the colours,
the typefaces, every app icon, the macOS DMG backgrounds and a snapshot of the Nodalia Design
Language (NDL) guide. The website (`nodalia-web`), `nodalia-design`, `nodalix-icon-theme` and each
app keep their own working copies; this folder is the reference set and the backup.

Collected on 2026-11-18 from `nodalia-web` (`assets/`), `nodalia-design` (`docs/`,
`packages/fonts`, `packages/tokens`, `packages/egui/crate/fonts`, `tools/`), `nodalix-icon-theme`
(`src/apps/scalable`) and each app's repository.

## Layout

| Path | What it is | Comes from |
|---|---|---|
| `logo/` | The mark, the wordmarks and the website icons, as SVG | `nodalia-web/assets` |
| `logo/png/` | PNG renders of the marks (512 px) and wordmarks (256 px high), for places that take no SVG | rendered here from `logo/*.svg` |
| `app-icons/*.png`, `*.svg` | Every app's icon, 512 × 512 (Brújula and Nodalix OS as SVG) | each app's repository; Luz rendered from its theme SVG |
| `app-icons/linux-theme/` | The same portraits fitted to the Colloid tile, as Nodalix OS shows them (`dev.danielmiguelt.<App>.svg`) | `nodalix-icon-theme/src/apps/scalable` |
| `fonts/` | Sora, Inter, IBM Plex Sans and IBM Plex Mono, each with its `OFL.txt` | `nodalia-design` |
| `dmg-backgrounds/` | The Finder window background of every app's macOS DMG: SVG master and a 2× PNG (1320 × 800) | generated with `nodalia-design/tools/dmg-background` |
| `ndl/` | The NDL guide: design language, tokens, components, iconography, the Creator and Engineering suite specs, and the token JSON files | `nodalia-design/docs`, `packages/tokens/src` |

`nodalia-design` stays the source for NDL and the fonts, and keeps the two generators (`tools/app-portrait` for the icon portraits, `tools/dmg-background` for the DMG windows); and each app's repository for
its icon. When one of them changes, refresh the copy here.

## Logo

| File | Use |
|---|---|
| `logo/nodalia-mark.svg` | The mark on its dark rounded tile: the default square logo (avatars, social cards) |
| `logo/nodalia-mark-bare.svg` | The mark alone, light, for dark backgrounds |
| `logo/nodalia-mark-bare-dark.svg` | The mark alone, dark, for light backgrounds |
| `logo/nodalia-logo.svg` | The mark as the website header uses it |
| `logo/nodalia-wordmark.svg` | Mark and name, as on the website |
| `logo/nodalia-wordmark-white.svg` | Mark and name, light, for dark backgrounds |
| `logo/nodalia-wordmark-black.svg` | Mark and name, dark, for light backgrounds |
| `logo/nodalia-wordmark-badge.svg` | Mark and name on a dark badge that reads on light and dark pages (README headers) |
| `logo/nodalia-placa-preview.png` | The wordmark plate on light and on dark, 1440 × 300: a reference, not a master |
| `logo/favicon.svg`, `favicon.ico`, `apple-touch-icon.png` | Browser and home-screen icons |

The mark is an `n` built from one bar and one arch, with a small square at its foot, the node,
filled with the only gradient the brand uses. It is drawn on a 64 × 64 grid. The wordmark is lower
case: `nodalia`.

In a README that follows GitHub's theme:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/getnodalia/foundation/main/brand/logo/nodalia-wordmark-white.svg">
  <img src="https://raw.githubusercontent.com/getnodalia/foundation/main/brand/logo/nodalia-wordmark-black.svg" width="150" alt="Nodalia">
</picture>
```

## Colour

| Role | Value |
|---|---|
| Ink (tile, text on light) | `#0B0D13` |
| Paper (mark and text on dark) | `#F4F5F9` |
| Node gradient | `#8ADBE0` → `#A79BFF` |
| Website background, surfaces | `#07080C`, `#11131B`, `#171A24` |

The gradient lives only in the node of the mark. Nothing else in the identity or the interfaces
uses a gradient or a glow. Inside the apps every colour comes from the NDL tokens (`ndl/tokens.md`,
`ndl/tokens/*.json`); each app adds a single accent, the colour of its icon
(`ndl/tokens/accents.json`):

| App | Accent | Suite | Icon portrait |
|---|---|---|---|
| Ágora | `#0F7C80` | Communication | Socrates |
| Ánima | `#6B4CE8` | Creator | Émile Cohl |
| Brújula | `#0C9A58` | Browser | Juan Sebastián Elcano |
| Buzón | `#D4241B` | Communication | Rowland Hill |
| Celdas | `#1D6B3B` | Office | Blaise Pascal |
| Forja | `#96501F` | Engineering | Leonardo da Vinci |
| Hito | `#3D9A2B` | Office | Henry Gantt (icon not released yet) |
| Lámina | `#7C1F41` | Office | Cicero |
| Letra | `#1C86D2` | Office | Miguel de Cervantes |
| Lienzo | `#EE3B6B` | Creator | Diego Velázquez |
| Luz | `#F59300` | Creator | Louis Daguerre |
| Nodalix OS | `#0A93B8` | Operating system | (Nodalix mark) |
| Papel | `#68778F` | Office | Aldus Manutius |
| Pliego | `#3340D0` | Creator | Johannes Gutenberg |
| Pluma | `#EE5A14` | Creator | René Descartes |
| Pulso | `#6FB312` | Creator | Eadweard Muybridge |
| Toma | `#C2188F` | Creator | Georges Méliès |
| Torno | `#8C7419` | Engineering | Henry Maudslay |
| Trama | `#8B2FD6` | Creator | Joseph Marie Jacquard |
| Vinilo | `#5A27D6` | Music | Ludwig van Beethoven |
| Vortia | `#0B55DB` | Engineering | Daniel Bernoulli |

## Type

| Typeface | Use | Licence |
|---|---|---|
| Sora | Titles and the bold display type of NDL; the wordmark and the DMG backgrounds | SIL OFL 1.1 |
| Inter | Interface and body text | SIL OFL 1.1 |
| IBM Plex Sans, IBM Plex Mono | The Engineering suite (Torno, Vortia, Forja): panels, values, coordinates | SIL OFL 1.1 |

The licence travels with each font in `fonts/<family>/OFL.txt`. Apps take their fonts from
`nodalia-design` or the `vendor/craft-fonts/main` branch of this repository, not from here.

## App icons

Every Nodalia app icon is a portrait of a historical figure tied to what the app does, cut out in
black and white on a full-bleed field of the app's accent, on a 512 tile with a 112 radius. The
portraits come from public-domain sources, recorded in each app's `ATTRIBUTION` and
`assets/app-icon/README.md`; the illustrations are Nodalia's own work. A new app gets its own
figure, made with `nodalia-design/tools/app-portrait`. The rule is in `ndl/iconography.md`.

`nodalix-icon-theme` keeps the icons of third-party applications as they are; only Nodalia's own
apps use the portraits.

## DMG backgrounds

Each app's DMG opens on its own Finder window: a coloured island on the left with a drawing of
what the app does, the app and Applications icons on a white island, and an arrow in the app's
colour. Flat colours, no gradients, text in outlined Sora. Apps keep the generated SVG in
`packaging/macos/dmg/` and convert it there; to change a drawing, edit
`tools/dmg-background/draw_background.py` in `nodalia-design` and regenerate.

## Using the brand

- Light marks on dark backgrounds, dark ones on light. Do not recolour, outline, shadow, rotate,
  stretch or redraw them.
- Leave clear space around a logo of at least the height of the node, and do not show the mark
  below 16 px or the wordmark below 80 px wide.
- An app's icon is its own; the Nodalia mark never replaces it and is never put inside it.
- The files are original Nodalia work published in this repository, the fonts excepted (OFL). The
  Nodalia name, the mark and the app icons identify Nodalia and its apps: use them unmodified to
  refer to Nodalia or one of its apps, and do not combine them with another name.

Brand changes are decided by Daniel. A change here goes with the same change in
`nodalia-web/assets` and `nodalia-design`, so the copies do not drift.
