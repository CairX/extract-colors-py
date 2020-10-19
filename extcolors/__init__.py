import collections

from convcolors import rgb_to_lab
from PIL import Image, ImageDraw

from extcolors import difference

__version__ = "1.0.0"

DEFAULT_TOLERANCE = 32


class Color:
    def __init__(self, rgb=None, lab=None, count=0):
        self.rgb = rgb
        self.lab = lab
        self.count = count
        self.compressed = False

    def __lt__(self, other):
        return self.count < other.count


def extract_from_image(img, tolerance=DEFAULT_TOLERANCE, limit=None):
    pixels = _load(img)
    pixel_count = len(pixels)
    pixels = _filter_fully_transparent(pixels)
    pixels = _strip_alpha(pixels)
    colors = _count_colors(pixels)
    colors = _compress(colors, tolerance)

    if limit:
        limit = min(int(limit), len(colors))
        colors = colors[:limit]

    colors = [(color.rgb, color.count) for color in colors]

    return colors, pixel_count


def extract_from_path(path, tolerance=DEFAULT_TOLERANCE, limit=None):
    img = Image.open(path)
    return extract_from_image(img, tolerance, limit)


def _load(img):
    img = img.convert("RGBA")
    return list(img.getdata())


def _filter_fully_transparent(pixels):
    return [p for p in pixels if p[3] > 0]


def _strip_alpha(pixels):
    return [(p[0], p[1], p[2]) for p in pixels]


def _count_colors(pixels):
    counter = collections.defaultdict(int)
    for color in pixels:
        counter[color] += 1

    colors = []
    for rgb, count in counter.items():
        lab = rgb_to_lab(rgb)
        colors.append(Color(rgb=rgb, lab=lab, count=count))

    return colors


def _compress(colors, tolerance):
    colors.sort(reverse=True)

    if tolerance <= 0:
        return colors

    i = 0
    while i < len(colors):
        larger = colors[i]

        if not larger.compressed:
            j = i + 1
            while j < len(colors):
                smaller = colors[j]

                if not smaller.compressed and difference.cie76(
                        larger.lab, smaller.lab) < tolerance:
                    larger.count += smaller.count
                    smaller.compressed = True

                j += 1
        i += 1

    colors = [color for color in colors if not color.compressed]
    colors.sort(reverse=True)

    return colors
