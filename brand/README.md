# Nodalia brand

The Nodalia logo, its wordmarks and the icon of every app, kept in one place so any repository,
website or document can take them from here. The website (`getnodalia/nodalia-web`) and each app's
repository keep their own copies; this folder is the reference set.

## Logo

| File | Use |
|---|---|
| [`logo/nodalia-mark.svg`](logo/nodalia-mark.svg) | The mark alone, on its dark rounded square |
| [`logo/nodalia-logo.svg`](logo/nodalia-logo.svg) | The mark as the website uses it in its header |
| [`logo/nodalia-wordmark.svg`](logo/nodalia-wordmark.svg) | Mark and name, as on the website |
| [`logo/nodalia-wordmark-badge.svg`](logo/nodalia-wordmark-badge.svg) | Mark and name on a badge that reads on light and dark pages (README headers) |
| [`logo/nodalia-wordmark-black.svg`](logo/nodalia-wordmark-black.svg) | Mark and name for light backgrounds |
| [`logo/nodalia-wordmark-white.svg`](logo/nodalia-wordmark-white.svg) | Mark and name for dark backgrounds |
| [`logo/favicon.svg`](logo/favicon.svg), [`logo/favicon.ico`](logo/favicon.ico), [`logo/apple-touch-icon.png`](logo/apple-touch-icon.png) | Browser and home-screen icons |

To show the logo in a README that follows GitHub's light or dark theme:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/getnodalia/foundation/main/brand/logo/nodalia-wordmark-white.svg">
  <img src="https://raw.githubusercontent.com/getnodalia/foundation/main/brand/logo/nodalia-wordmark-black.svg" width="150" alt="Nodalia">
</picture>
```

## Colour and type

- The mark's gradient runs from `#8ADBE0` (cyan) to `#A79BFF` (violet) on `#0B0D13`.
- The website's base: background `#07080C`, surfaces `#11131B` and `#171A24`, text `#F4F5F9`,
  accent `#8ADBE0`.
- Type: **Sora** for headings and **Inter** for text (both SIL OFL 1.1). Apps take their fonts from
  the `vendor/craft-fonts/main` branch of this repository.
- Inside the apps, every colour comes from the Nodalia Design Language tokens in
  [nodalia-design](https://github.com/getnodalia/nodalia-design) (`docs/tokens.md`), never from
  this page.
- No decorative gradients or glows in the interfaces: the gradient belongs to the mark.

## App icons

Every app's icon is a portrait of a historical figure tied to what the app does; the list of
figures and the tool that draws them live in nodalia-design. The files here are 512 × 512 PNG
copies taken from each app's repository on 2026-11-18 (Brújula and Nodalix OS are SVG). The app's
own repository stays the source when an icon changes.

| App | File | Suite or category | Accent |
|---|---|---|---|
| Ágora | [`agora.png`](app-icons/agora.png) | Communication | teal `#0F7C80` |
| Ánima | [`anima.png`](app-icons/anima.png) | Creator | periwinkle |
| Brújula | [`brujula.svg`](app-icons/brujula.svg) | Browser | green |
| Buzón | [`buzon.png`](app-icons/buzon.png) | Communication | scarlet `#D4241B` |
| Celdas | [`celdas.png`](app-icons/celdas.png) | Office | emerald |
| Forja | [`forja.png`](app-icons/forja.png) | Engineering | copper |
| Lámina | [`lamina.png`](app-icons/lamina.png) | Office | magenta |
| Letra | [`letra.png`](app-icons/letra.png) | Office | azure |
| Lienzo | [`lienzo.png`](app-icons/lienzo.png) | Creator | rose |
| Nodalix OS | [`nodalix.svg`](app-icons/nodalix.svg) | Operating system | blue |
| Papel | [`papel.png`](app-icons/papel.png) | Office | slate |
| Pliego | [`pliego.png`](app-icons/pliego.png) | Creator | indigo |
| Pluma | [`pluma.png`](app-icons/pluma.png) | Creator | orange |
| Pulso | [`pulso.png`](app-icons/pulso.png) | Creator | lime |
| Toma | [`toma.png`](app-icons/toma.png) | Creator | fuchsia |
| Torno | [`torno.png`](app-icons/torno.png) | Engineering | gold |
| Trama | [`trama.png`](app-icons/trama.png) | Creator | lilac `#7A26C9` |
| Vinilo | [`vinilo.png`](app-icons/vinilo.png) | Music | violet |
| Vortia | [`vortia.png`](app-icons/vortia.png) | Engineering | azure |

## Using the marks

The Nodalia name, the mark and the app icons identify Nodalia and its apps. Use them unmodified
to refer to Nodalia or one of its apps; do not recolour, redraw or combine them with another
name. They are not covered by the `MIT OR Apache-2.0` licence of the code in this repository.
