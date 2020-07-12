# coding: utf8

import argparse
import math
import os
import time

from PIL import Image, ImageDraw

from extcolors import DEFAULT_TOLERANCE, extract_from_path


def print_result(colors, total):
    print("Extracted colors:")
    for color in colors:
        rgb = str(color[0])
        count = color[1]
        percentage = "{0:.2f}".format((float(count) / float(total)) * 100.0)
        print("{0:15}:{1:>7}% ({2})".format(rgb, percentage, count))

    pixel_count = sum([color[1] for color in colors])
    print("\nPixels in output: {} of {}".format(pixel_count, total))


def image_result(colors, size, filename):
    columns = 5
    width = int(min(len(colors), columns) * size)
    height = int((math.floor(len(colors) / columns) + 1) * size)

    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(result)
    for idx, color in enumerate(colors):
        x = int((idx % columns) * size)
        y = int(math.floor(idx / columns) * size)
        canvas.rectangle([(x, y), (x + size - 1, y + size - 1)],
                         fill=color[0])

    filename = "{0} {1}.png".format(
        filename, time.strftime("%Y-%m-%d %H%M%S", time.localtime()))
    result.save(filename, "PNG")


def parse_tolerance(value):
    value = float(value)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError(
            "{} isn't a integer between 0 and 100".format(value))
    return value


def parse_limit(value):
    value = int(value)
    if value < 0:
        raise argparse.ArgumentTypeError(
            "{} isn't a positive integer".format(value))
    return value


def main():
    parser = argparse.ArgumentParser(
        description="Extract colors from a specified image. "
        "Colors are grouped based on visual similarities using the CIE76 formula."
    )
    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s 0.1.2")
    parser.add_argument("image", nargs=1, metavar="PATH")
    parser.add_argument(
        "-t",
        "--tolerance",
        nargs="?",
        type=parse_tolerance,
        default=DEFAULT_TOLERANCE,
        const=DEFAULT_TOLERANCE,
        metavar="N",
        help=
        "Group colors to limit the output and give a better visual representation. "
        "Based on a scale from 0 to 100. Where 0 won't group any color and 100 will group all colors into one. "
        "Tolerance 0 will bypass all conversion. "
        "Defaults to {0}.".format(DEFAULT_TOLERANCE))
    parser.add_argument(
        "-l",
        "--limit",
        nargs="?",
        type=parse_limit,
        metavar="N",
        help=
        "Upper limit to the number of extracted colors presented in the output."
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=["all", "image", "text"],
        default="all",
        help="Format(s) that the extracted colors should presented in.")
    args = parser.parse_args()

    path = args.image[0]
    filename = os.path.splitext(os.path.basename(path))[0]
    colors, total = extract_from_path(path, args.tolerance, args.limit)

    if args.output in ["all", "text"]:
        print_result(colors, total)
    if args.output in ["all", "image"]:
        image_result(colors, 150, filename)
