# coding: utf8

import argparse
import extcolors.colorutil
import math
import os
import time
from collections import defaultdict
from PIL import Image, ImageDraw


DEFAULT_TOLERANCE = 32


def extract(path, tolerance=DEFAULT_TOLERANCE, limit=None):
	pixels = load(path)
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

def to_int(tuple):
	return int(tuple[0]), int(tuple[1]), int(tuple[2])

def load(path):
	img = Image.open(path)
	img = img.convert("RGB")
	return list(img.getdata())


def count_colors(pixels):
	counter = defaultdict(int)
	for color in pixels:
		counter[color] += 1
	return counter


def compress(counter, tolerance):
	result = counter
	if tolerance <= 0:
		return result

	colors = [item[0] for item in sorted(counter.items(), key=lambda x: x[1], reverse=True)]
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


def print_result(counter, total):
	print("Extracted colors:")
	for key, value in counter:
		print("{0:15}:{1:>7}% ({2})".format(str(key), "{0:.2f}".format((float(value) / float(total)) * 100.0), value))
	print("\nPixels in output: {} of {}".format(sum([c[1] for c in counter]), total))


def image_result(counter, size, filename):
	columns = 5
	width = int(min(len(counter), columns) * size)
	height = int((math.floor(len(counter) / columns) + 1) * size)

	result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
	canvas = ImageDraw.Draw(result)
	for idx, item in enumerate(counter):
		x = int((idx % columns) * size)
		y = int(math.floor(idx / columns) * size)
		canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill=item[0])

	filename = "{0} {1}.png".format(filename, time.strftime("%Y-%m-%d %H%M%S", time.localtime()))
	result.save(filename, "PNG")


def parse_tolerance(value):
	value = float(value)
	if value < 0 or value > 100:
		raise argparse.ArgumentTypeError("{} isn't a integer between 0 and 100".format(value))
	return value


def parse_limit(value):
	value = int(value)
	if value < 0:
		raise argparse.ArgumentTypeError("{} isn't a positive integer".format(value))
	return value


def main():
	parser = argparse.ArgumentParser(
		description="Extract colors from a specified image. "
					"Colors are grouped based on visual similarities using the CIE76 formula."
	)
	parser.add_argument(
		"--version",
		action="version",
		version="%(prog)s 0.1.2"
	)
	parser.add_argument(
		"image",
		nargs=1,
		metavar="PATH"
	)
	parser.add_argument(
		"-t", "--tolerance",
		nargs="?",
		type=parse_tolerance,
		default=DEFAULT_TOLERANCE,
		const=DEFAULT_TOLERANCE,
		metavar="N",
		help="Group colors to limit the output and give a better visual representation. "
			"Based on a scale from 0 to 100. Where 0 won't group any color and 100 will group all colors into one. "
			"Tolerance 0 will also bypass all conversion. "
			"Defaults to {0}.".format(DEFAULT_TOLERANCE)
	)
	parser.add_argument(
		"-l", "--limit",
		nargs="?",
		type=parse_limit,
		metavar="N",
		help="Upper limit to the number of extracted colors presented in the output."
	)
	parser.add_argument(
		"-o", "--output",
		choices=["all", "image", "text"],
		default="all",
		help="Format(s) that the extracted colors should presented in."
	)
	args = parser.parse_args()

	path = args.image[0]
	filename = os.path.splitext(os.path.basename(path))[0]
	counter, total = extract(path, args.tolerance, args.limit)

	if args.output in ["all", "text"]:
		print_result(counter, total)
	if args.output in ["all", "image"]:
		image_result(counter, 150, filename)


if __name__ == "__main__":
	main()
