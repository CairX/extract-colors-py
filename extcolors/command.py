import argparse
import math
import os
import time

from PIL import Image, ImageDraw

from extcolors import __version__, DEFAULT_TOLERANCE, extract_from_path


def print_result(colors, pixel_count):
    print("Extracted colors:")
    color_count = sum([color[1] for color in colors])
    for color in colors:
        rgb = str(color[0])
        count = color[1]
        percentage = "{:.2f}".format((float(count) / float(color_count)) * 100.0)
        print(f"{rgb:15}:{percentage:>7}% ({count})")

    print(f"\nPixels in output: {color_count} of {pixel_count}")


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

    result.save(filename, "PNG")


def gimp_color_palette_result(colors, filename, palette):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"GIMP Palette\nName: {palette}\n")
        for color in colors:
            rgb = color[0]
            file.write("{}\t{}\t{}\n".format(rgb[0], rgb[1], rgb[2]))


def parse_tolerance(value):
    value = float(value)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError(
            f"{value} isn't a integer between 0 and 100")
    return value


def parse_limit(value):
    value = int(value)
    if value < 0:
        raise argparse.ArgumentTypeError(
            f"{value} isn't a positive integer")
    return value


def construct_filename(original, custom, timestamp, extension):
    filename = ""
    if isinstance(custom, str):
        filename = custom
        if not filename.endswith(extension):
            filename = f"{filename}{extension}"
    else:
        filename = f"{original} {timestamp}{extension}"
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="Extract colors from a specified image. "
        "Colors are grouped based on visual similarities using the CIE76 formula."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument("path", nargs=1, metavar="PATH")
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
        "Defaults to {}.".format(DEFAULT_TOLERANCE))
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
        "-s",
        "--silence",
        action="store_true",
        help=
        "Silences the default output. "
        "Doesn't effect any other output option."
    )
    parser.add_argument(
        "-i",
        "--image",
        nargs="?",
        default=None,
        const=True,
        metavar="NAME",
        help=
        "Output the result to an image palette. "
        "A name for the file can be supplied."
    )
    parser.add_argument(
        "-g",
        "--gpl",
        nargs="?",
        default=None,
        const=True,
        metavar="NAME",
        help=
        "Output the result to a GIMP color palette (GPL). "
        "A name for the palette can be supplied."
    )
    args = parser.parse_args()

    path = args.path[0]
    original_filename = os.path.splitext(os.path.basename(path))[0]
    colors, total = extract_from_path(path, args.tolerance, args.limit)
    timestamp = time.strftime("%Y-%m-%d %H%M%S", time.localtime())

    if not args.silence:
        print_result(colors, total)
    if args.image:
        filename = construct_filename(original_filename, args.image, timestamp, ".png")
        image_result(colors, 150, filename)
    if args.gpl:
        palette = args.gpl if isinstance(args.gpl, str) else original_filename
        filename = construct_filename(original_filename, args.gpl, timestamp, ".gpl")
        gimp_color_palette_result(colors, filename, palette)
