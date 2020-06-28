# coding: utf8

import collections

from PIL import Image, ImageDraw

from extcolors import colorutil

DEFAULT_TOLERANCE = 32


def extract_from_image(img, tolerance=DEFAULT_TOLERANCE, limit=None):
    pixels = load(img)
    rgb_colors = count_colors(pixels)

    if tolerance > 0:
        lab_colors = dict()
        for color, count in rgb_colors.items():
            lab_colors[colorutil.rgb_lab(color)] = count

        lab_colors = compress(lab_colors, tolerance)

        rgb_colors = dict()
        for color, count in lab_colors.items():
            rgb_colors[colorutil.lab_rgb(color)] = count

    rgb_colors = sorted(rgb_colors.items(), key=lambda x: x[1], reverse=True)
    rgb_colors = [(to_int(c[0]), c[1]) for c in rgb_colors]

    if limit:
        rgb_colors = rgb_colors[:min(int(limit), len(rgb_colors))]

    return rgb_colors, len(pixels)


def extract_from_path(path, tolerance=DEFAULT_TOLERANCE, limit=None):
    img = Image.open(path)
    return extract_from_image(img, tolerance, limit)


def to_int(tuple):
    return int(tuple[0]), int(tuple[1]), int(tuple[2])


def load(img):
    img = img.convert("RGB")
    return list(img.getdata())


def count_colors(pixels):
    counter = collections.defaultdict(int)
    for color in pixels:
        counter[color] += 1
    return counter


def compress(counter, tolerance):
    result = counter
    if tolerance <= 0:
        return result

    colors = [
        item[0]
        for item in sorted(counter.items(), key=lambda x: x[1], reverse=True)
    ]
    i = 0
    while i < len(colors):
        larger = colors[i]

        j = i + 1
        while j < len(colors):
            smaller = colors[j]
            if colorutil.cie76(smaller, larger) < tolerance:
                result[larger] += result[smaller]
                result.pop(smaller)
                colors.remove(smaller)
            else:
                j += 1
        i += 1

    return result
