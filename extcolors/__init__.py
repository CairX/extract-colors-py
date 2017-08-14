import argparse
import extcolors.colorutil
import math
import os
import time
from collections import defaultdict
from PIL import Image, ImageDraw


class Timer(object):
	def __init__(self):
		self.start = time.time()

	def elapsed(self):
		return time.time() - self.start


def extract(path, tolerance, limit=None):
	timer = Timer()
	pixels = load(path)

	counter = count_colors(pixels)
	tmp = dict()
	for color, count in counter.items():
		tmp[colorutil.rgb_lab(color)] = count

	counter = compress(tmp, tolerance)
	counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)

	if limit:
		counter = counter[:min(int(limit), len(counter))]

	counter = [(colorutil.lab_rgb(c[0]), c[1]) for c in counter]

	print("\nPixels in output: {} of {}".format(sum([c[1] for c in counter]), len(pixels)))
	print("Total time: {} seconds".format(timer.elapsed()))

	return counter, len(pixels)


def load(path):
	timer = Timer()
	img = Image.open(path)
	print(img.mode)
	img = img.convert("RGB")
	print(img.mode)
	pixels = list(img.getdata())
	width, height = img.size

	print("\n[IMAGE]")
	print("Width: {}".format(width))
	print("Height: {}".format(height))
	print("Pixels: {}".format(len(pixels)))
	print("Color profile: {}".format(img.info.get("icc_profile", "None specified")))
	print("Time: {} seconds".format(timer.elapsed()))

	return pixels


def count_colors(pixels):
	timer = Timer()
	counter = defaultdict(int)
	for color in pixels:
		counter[color] += 1

	print("\n[COUNT]")
	print("Colors: {}".format(len(counter)))
	print("Time: {} seconds".format(timer.elapsed()))

	return counter


def compress(counter, tolerance):
	result = counter
	if tolerance <= 0:
		return result

	timer = Timer()
	colors = [item[0] for item in sorted(counter.items(), key=lambda x: x[1], reverse=True)]

	cmp_times = list()
	i = 0
	while i < len(colors):
		cmp_timer = Timer()
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
		cmp_times.append(cmp_timer.elapsed())
		i += 1

	print("\n[COMPRESS]")
	print("Colors: {}".format(len(result)))
	print("Cmp time: {} seconds, {} times".format(sum(cmp_times), len(cmp_times)))
	print("Cmp avg. time: {} milliseconds".format(sum(cmp_times) * 1000 / len(cmp_times)))
	print("Time: {} seconds".format(timer.elapsed()))

	return result


def print_result(counter, total):
	print("\n[RESULT]")
	for key, value in counter:
		print("{0:15}:{1:>7}% ({2})".format(str(key), "{0:.2f}".format(value / total * 100), value))


def image_result(counter, size, filename):
	columns = 5
	width = min(len(counter), columns) * size
	height = (math.floor(len(counter) / columns) + 1) * size

	result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
	canvas = ImageDraw.Draw(result)
	for idx, item in enumerate(counter):
		x = (idx % columns) * size
		y = math.floor(idx / columns) * size
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
		version="%(prog)s 0.1.0"
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
		default=32,
		const=32,
		metavar="N",
		help="group colors to limit the output and give a better visual representation. "
			"Based on a scale from 0 to 100. Where 0 won't group any color and 100 will group all colors into one. "
			"Defaults to 32"
	)
	parser.add_argument(
		"-l", "--limit",
		nargs="?",
		type=parse_limit,
		metavar="N",
		help="upper limit to the number of extracted colors presented in the output"
	)
	parser.add_argument(
		"-o", "--output",
		choices=["all", "image", "text"],
		default="all",
		help="format(s) that the extracted colors should presented in"
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
