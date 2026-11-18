#!/usr/bin/env python3
"""Make a Nodalia app icon's artwork: a historical portrait cut out in black and white on the
app's colour field, full bleed, 1024 px (see README.md).

Usage:
  portrait.py SOURCE OUT.png --box L,T,R,B --colors TOP BOTTOM [--gamma G]
              [--model NAME] [--add-mask X,Y,X,Y,...] [--mask X,Y,X,Y,...]

SOURCE is the portrait as downloaded (any size); the figure is found on the whole image, then
the square BOX (pixels of SOURCE; it may reach past the edges) is what fills the tile. Needs
Pillow and rembg (`pip install "rembg[cpu]"`; the model downloads on first use).
"""
import argparse

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps
from rembg import new_session, remove

SIZE = 1024


def numbers(text):
    return [int(v) for v in text.split(',')]


def rgb(hex_colour):
    h = hex_colour.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cut_out(image, model, extra):
    # Matting keeps hair and fabric edges soft instead of stair-stepped.
    cut = remove(image, session=new_session(model), alpha_matting=True,
                 alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=15,
                 alpha_matting_erode_size=8)
    if extra:
        # Where the model loses a shoulder into a background of the same tone, a hand-drawn
        # polygon (pixels of SOURCE) adds it back.
        mask = Image.new('L', cut.size, 0)
        ImageDraw.Draw(mask).polygon(list(zip(extra[::2], extra[1::2])), fill=255)
        cut.putalpha(ImageChops.lighter(cut.getchannel('A'), mask.filter(ImageFilter.GaussianBlur(3))))
    return cut


def traced(image, outline):
    # Engravings put hatching behind the figure, which the model keeps as part of it; there the
    # figure is a hand-drawn outline (pixels of SOURCE) instead.
    mask = Image.new('L', image.size, 0)
    ImageDraw.Draw(mask).polygon(list(zip(outline[::2], outline[1::2])), fill=255)
    cut = image.convert('RGBA')
    cut.putalpha(mask.filter(ImageFilter.GaussianBlur(4)))
    return cut


def black_and_white(figure, gamma):
    grey = ImageOps.autocontrast(ImageOps.grayscale(figure.convert('RGB')), cutoff=0.5)
    if gamma != 1.0:
        grey = grey.point(lambda v: 255 * (v / 255) ** gamma)
    grey = ImageEnhance.Contrast(grey).enhance(1.15)
    return ImageEnhance.Sharpness(grey).enhance(1.4)


def field(top, bottom):
    t, b = rgb(top), rgb(bottom)
    column = Image.new('RGB', (1, SIZE))
    for y in range(SIZE):
        k = y / (SIZE - 1)
        column.putpixel((0, y), tuple(round(t[i] + (b[i] - t[i]) * k) for i in range(3)))
    return column.resize((SIZE, SIZE)).convert('RGBA')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source')
    parser.add_argument('out')
    parser.add_argument('--box', type=numbers, required=True, help='L,T,R,B: the square that fills the tile')
    parser.add_argument('--colors', nargs=2, required=True, metavar=('TOP', 'BOTTOM'))
    parser.add_argument('--gamma', type=float, default=1.0, help='above 1 darkens the midtones')
    parser.add_argument('--model', default='u2net_human_seg')
    parser.add_argument('--add-mask', type=numbers, default=None, help='X,Y,X,Y,...: polygon added to the figure')
    parser.add_argument('--mask', type=numbers, default=None,
                        help='X,Y,X,Y,...: the figure is this polygon, without the model (engravings)')
    args = parser.parse_args()

    source = Image.open(args.source).convert('RGB')
    if args.mask:
        cut = traced(source, args.mask)
    else:
        cut = cut_out(source, args.model, args.add_mask)
    cut = cut.crop(tuple(args.box)).resize((SIZE, SIZE), Image.LANCZOS)
    alpha = cut.getchannel('A').filter(ImageFilter.GaussianBlur(1.2))

    canvas = field(*args.colors)
    # A soft shadow just behind the figure lifts it off the colour.
    shadow = Image.new('L', (SIZE, SIZE), 0)
    shadow.paste(alpha.point(lambda v: v * 0.35).filter(ImageFilter.GaussianBlur(18)), (6, 10))
    layer = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    layer.putalpha(shadow)
    canvas = Image.alpha_composite(canvas, layer)
    figure = black_and_white(cut, args.gamma).convert('RGBA')
    figure.putalpha(alpha)
    Image.alpha_composite(canvas, figure).convert('RGB').save(args.out)


if __name__ == '__main__':
    main()
