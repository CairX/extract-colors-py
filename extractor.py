import argparse
import colorutil
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


def load(path):
	timer = Timer()
	img = Image.open(path)
	print(img.mode)
	# TODO Handle alpha.
	img = img.convert("RGB")
	print(img.mode)
	pixels = list(img.getdata())
	width, height = img.size

	print("\n[IMAGE]")
	print("Width: {}".format(width))
	print("Height: {}".format(height))
	print("Pixels: {}".format(len(pixels)))
	print("Color profile: {}".format(img.info.get("icc_profile", "")))
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

	# TODO Sort before each loop?
	# TODO Prevent more than 1% chained combination steps, probably.
	# TODO Speed up.
	# TODO Handle cases when items are equal in size. The result should be consistent.
	diff_times = list()
	cmp_times = list()
	i = 0
	while i < len(colors):
		cmp_timer = Timer()
		larger = colors[i]

		j = i + 1
		while j < len(colors):
			smaller1 = colors[j]
			diff_timer = Timer()
			ndiff = colorutil.cie76(smaller1, larger)
			diff_times.append(diff_timer.elapsed())

			# http://zschuessler.github.io/DeltaE/learn/
			if ndiff < tolerance:
				result[larger] += result[smaller1]
				result.pop(smaller1)
				colors.remove(smaller1)
			else:
				j += 1
		cmp_times.append(cmp_timer.elapsed())
		i += 1

	print("\n[COMPRESS]")
	print("Colors: {}".format(len(result)))
	print("Diff time: {} seconds, {} times".format(sum(diff_times), len(diff_times)))
	print("Diff avg. time: {} milliseconds".format(sum(diff_times) * 1000 / len(diff_times)))
	print("Cmp time: {} seconds, {} times".format(sum(cmp_times), len(cmp_times)))
	print("Cmp avg. time: {} milliseconds".format(sum(cmp_times) * 1000 / len(cmp_times)))
	print("Time: {} seconds".format(timer.elapsed()))

	return result


def print_result(counter, total):
	print("\n[RESULT]")
	for key, value in counter:
		print("{0:15}:{1:>7}% ({2})".format(str(key), "{0:.2f}".format(value / total * 100), value))


def image_result(counter, size, path):
	columns = 5
	width = min(len(counter), columns) * size
	height = (math.floor(len(counter) / columns) + 1) * size

	result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
	canvas = ImageDraw.Draw(result)
	for idx, item in enumerate(counter):
		c = round(item[0][0]), round(item[0][1]), round(item[0][2])
		x = (idx % columns) * size
		y = math.floor(idx / columns) * size
		w = size - 1
		h = size - 1
		canvas.rectangle([(x, y), (x + w, y + h)], fill=c)

	file_name = os.path.splitext(os.path.basename(path))[0]
	file_name = "{0} {1}.png".format(file_name, time.strftime("%Y-%m-%d %H%M%S", time.localtime()))
	result.save(os.path.join("results", file_name), "PNG")


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
	timer = Timer()
	parser = argparse.ArgumentParser(
		description="Extract the most common colors from an image.")
	parser.add_argument(
		"image",
		nargs=1,
		metavar="PATH")
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
		help="upper limit to the number of extracted colors presented in the output",
	)
	args = parser.parse_args()

	path = args.image[0]
	pixels = load(path)

	counter = count_colors(pixels)
	tmp = dict()
	for color, count in counter.items():
		tmp[colorutil.rgb_lab(color)] = count

	counter = compress(tmp, args.tolerance)
	counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)

	if args.limit:
		counter = counter[:min(int(args.limit), len(counter))]

	# TODO Restore to int instead of float.
	counter = [(colorutil.lab_rgb(c[0]), c[1]) for c in counter]
	print_result(counter, len(pixels))
	image_result(counter, 150, filename)

	print("\nPixels in output: {} of {}".format(sum([c[1] for c in counter]), len(pixels)))
	print("Total time: {} seconds".format(timer.elapsed()))


if __name__ == "__main__":
	main()
