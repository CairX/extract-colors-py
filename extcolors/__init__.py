# coding: utf8

import collections

from PIL import Image, ImageDraw

from extcolors import conversion
from extcolors import difference

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
    pixels = load(img)
    colors = count_colors(pixels)
    colors = compress(colors, tolerance)

    if limit:
        limit = min(int(limit), len(colors))
        colors = colors[:limit]

    colors = [(color.rgb, color.count) for color in colors]

    return colors, len(pixels)


def extract_from_path(path, tolerance=DEFAULT_TOLERANCE, limit=None):
    img = Image.open(path)
    return extract_from_image(img, tolerance, limit)


def load(img):
    img = img.convert("RGB")
    return list(img.getdata())


def count_colors(pixels):
    counter = collections.defaultdict(int)
    for color in pixels:
        counter[color] += 1

    colors = []
    for rgb, count in counter.items():
        lab = conversion.rgb_lab(rgb)
        colors.append(Color(rgb=rgb, lab=lab, count=count))

    return colors


def compress(colors, tolerance):
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
