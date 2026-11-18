#!/usr/bin/env python3
"""Derive the Nodalia logo variants from the master SVGs in this folder and render the PNGs.

The masters are nodalia-mark.svg (the mark on its tile) and nodalia-wordmark-black.svg (mark and
name). Everything else here is written by this script: light and dark, monochrome, the name alone,
plates, and PNGs at fixed sizes under png/. Run it after changing a master:

    pip install cairosvg pillow
    python3 brand/logo/render.py
"""

import re
from pathlib import Path

import cairosvg

HERE = Path(__file__).resolve().parent
INK = "#0B0D13"
PAPER = "#F4F5F9"
EDGE_DARK = "#2C313C"
EDGE_LIGHT = "#D9DCE3"
GRADIENT = (
    '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#8ADBE0"/><stop offset="1" stop-color="#A79BFF"/>'
    "</linearGradient></defs>"
)
N_PATH = "M10 56V10h14v8a19 19 0 0 1 30 15v5H40v-5a8 8 0 0 0-16 0v23z"
NAME_BOX = "83.6 5.3 167.8 43.9"  # the name's own bounds in the wordmark's 251 x 64 grid

MARK_SIZES = (16, 32, 48, 64, 128, 256, 512, 1024)
WIDE_HEIGHTS = (64, 128, 256, 512)


def name_path() -> str:
    text = (HERE / "nodalia-wordmark-black.svg").read_text()
    found = re.findall(r'<path fill="[^"]+" d="([^"]+)"', text)
    if not found:
        raise SystemExit("no name path in nodalia-wordmark-black.svg")
    return found[-1]


def svg(view_box: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" role="img" '
        f'aria-label="Nodalia">{GRADIENT}{body}</svg>\n'
    )


def mark(fill: str, node: str) -> str:
    return f'<path d="{N_PATH}" fill="{fill}"/><rect x="40" y="43" width="14" height="13" rx="2" fill="{node}"/>'


def tile(bg: str, fill: str, node: str) -> str:
    return (
        f'<rect width="64" height="64" rx="15" fill="{bg}"/>'
        f'<g transform="translate(8.96 8.9) scale(.72)">{mark(fill, node)}</g>'
    )


def wordmark(fill: str, node: str, name: str) -> str:
    return mark(fill, node) + f'<path fill="{fill}" d="{name}"/>'


def plate(bg: str, edge: str, inner: str) -> str:
    return (
        f'<rect x="0.5" y="0.5" width="290" height="83" rx="20" fill="{bg}" stroke="{edge}"/>'
        f'<g transform="translate(20 10)">{inner}</g>'
    )


def variants(name: str) -> dict[str, tuple[str, str]]:
    grad = "url(#g)"
    return {
        # name: (viewBox, body)
        "nodalia-mark-light": ("0 0 64 64", tile(PAPER, INK, grad)),
        "nodalia-mark-mono-black": ("8 8 48 48", mark(INK, INK)),
        "nodalia-mark-mono-white": ("8 8 48 48", mark(PAPER, PAPER)),
        "nodalia-wordmark-mono-black": ("0 0 251 64", wordmark(INK, INK, name)),
        "nodalia-wordmark-mono-white": ("0 0 251 64", wordmark(PAPER, PAPER, name)),
        "nodalia-name-black": (NAME_BOX, f'<path fill="{INK}" d="{name}"/>'),
        "nodalia-name-white": (NAME_BOX, f'<path fill="{PAPER}" d="{name}"/>'),
        "nodalia-wordmark-badge-light": ("0 0 291 84", plate(PAPER, EDGE_LIGHT, wordmark(INK, grad, name))),
    }


def social_card(name: str) -> str:
    # 1200 x 630 card for link previews: the light wordmark centred on ink.
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-label="Nodalia">'
        f'{GRADIENT}<rect width="1200" height="630" fill="{INK}"/>'
        f'<g transform="translate(286 235) scale(2.5)">{wordmark(PAPER, "url(#g)", name)}</g></svg>\n'
    )


def render(src: Path, out: Path, width: int | None = None, height: int | None = None) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(url=str(src), write_to=str(out), output_width=width, output_height=height)


def main() -> None:
    name = name_path()
    for stem, (box, body) in variants(name).items():
        (HERE / f"{stem}.svg").write_text(svg(box, body))
    (HERE / "nodalia-social-card.svg").write_text(social_card(name))

    square = ["nodalia-mark", "nodalia-mark-light", "nodalia-mark-bare", "nodalia-mark-bare-dark",
              "nodalia-mark-mono-black", "nodalia-mark-mono-white"]
    wide = ["nodalia-wordmark-white", "nodalia-wordmark-black", "nodalia-wordmark-mono-black",
            "nodalia-wordmark-mono-white", "nodalia-wordmark-badge", "nodalia-wordmark-badge-light",
            "nodalia-name-black", "nodalia-name-white"]
    for stem in square:
        for size in MARK_SIZES:
            render(HERE / f"{stem}.svg", HERE / "png" / stem / f"{size}.png", size, size)
    for stem in wide:
        for h in WIDE_HEIGHTS:
            render(HERE / f"{stem}.svg", HERE / "png" / stem / f"{h}h.png", height=h)
    render(HERE / "nodalia-social-card.svg", HERE / "png" / "nodalia-social-card.png", 1200, 630)


if __name__ == "__main__":
    main()
