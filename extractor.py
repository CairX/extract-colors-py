import argparse
import os
import time
from collections import defaultdict
from PIL import Image, ImageDraw


def load(path):
	im = Image.open(path)
	pixels = list(im.getdata())
	width, height = im.size

	print("\n[IMAGE]")
	print("Width: {}".format(width))
	print("Height: {}".format(height))
	print("Pixels: {}".format(len(pixels)))

	return pixels


def count_colors(pixels):
	counter = defaultdict(int)
	for color in pixels:
		counter[color] += 1

	print("\n[COUNTER]")
	print("Colors: {}".format(len(counter)))

	return sorted(counter.items(), key=lambda x: x[1], reverse=True)


def print_result(counter, total):
	print("\n[RESULT]")
	for key, value in counter:
		print("{0:15}:{1:>7}% ({2})".format(str(key), "{0:.2f}".format(value / total * 100), value))


def image_result(counter, size, path):
	result = Image.new("RGBA", (len(counter) * size, size), (0, 0, 0, 0))
	canvas = ImageDraw.Draw(result)
	for idx, item in enumerate(counter):
		canvas.rectangle([(idx * size, 0), ((idx * size) + (size - 1), (size - 1))], fill=item[0])

	file_name = os.path.splitext(os.path.basename(path))[0]
	file_name = "{0} {1}.png".format(file_name, time.strftime("%Y-%m-%d %H%M%S", time.gmtime()))
	result.save(os.path.join("results", file_name), "PNG")


def main():
	parser = argparse.ArgumentParser(
		description="Extract the most common colors from an image.")
	parser.add_argument(
		"image",
		nargs=1,
		metavar="PATH")
	args = parser.parse_args()

	path = args.image[0]
	pixels = load(path)
	counter = count_colors(pixels)
	wanted = min(10, len(counter))
	counter = counter[:wanted]

	print_result(counter, len(pixels))
	image_result(counter, 150, path)


if __name__ == "__main__":
	main()
