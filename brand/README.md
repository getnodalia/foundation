# Nodalia brand

The Nodalia mark and wordmark, the source for every repository, the website and the apps. The
website (`getnodalia/nodalia-web`) serves copies from its `assets/`; this folder keeps the originals.

| File | Use |
|---|---|
| `nodalia-mark.svg` | The mark on its dark rounded tile: avatars, app launchers, social cards |
| `nodalia-favicon.svg` | The mark alone; ink follows the browser's light or dark theme |
| `favicon.ico`, `png/apple-touch-icon.png` | Fallbacks for browsers and iOS |
| `nodalia-wordmark-white.svg` | Mark and name in light ink, for dark backgrounds |
| `nodalia-wordmark-black.svg` | Mark and name in dark ink, for light backgrounds |
| `nodalia-wordmark-badge.svg` | The wordmark on its own tile, readable on light and dark pages alike |
| `png/` | The same at 512 px high (the mark at 1024 px), transparent background |

In a README, show the white and black wordmarks with `<picture>` and `prefers-color-scheme` so
GitHub picks the right one in each theme.

## Colours

| Token | Value | Where |
|---|---|---|
| Ink dark | `#0B0D13` | Tile, dark ink |
| Ink light | `#F4F5F9` | Light ink |
| Node gradient | `#8ADBE0` → `#A79BFF` (top left to bottom right) | The square node of the mark |

## Typography

Headings use Sora, text uses Inter (both SIL OFL 1.1). The font files are not kept here: they come
from the `nodalia/fonts` branch of this repository.

## Rules

- Use the files unmodified: don't redraw, recolour, stretch or add effects.
- Keep clear space around the mark of at least the width of its square node.
- The Nodalia name and logos are trademarks of the Nodalia project. They are not covered by the
  code licences (`LICENSE-MIT`, `LICENSE-APACHE`) of this repository, and forks and modified
  versions must not use them.
