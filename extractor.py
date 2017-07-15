import argparse
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
	img = img.convert("HSV")
	print(img.mode)
	pixels = list(img.getdata())
	width, height = img.size

	print("\n[IMAGE]")
	print("Width: {}".format(width))
	print("Height: {}".format(height))
	print("Pixels: {}".format(len(pixels)))
	print("Time: {} seconds".format(timer.elapsed()))

	return pixels


def count_colors(pixels):
	timer = Timer()
	counter = defaultdict(int)
	for color in pixels:
		counter[color] += 1
	counter = [list(item) for item in sorted(counter.items(), key=lambda x: x[1], reverse=True)]

	print("\n[COUNTER]")
	print("Colors: {}".format(len(counter)))
	print("Time: {} seconds".format(timer.elapsed()))

	return counter


def compress(counter):
	timer = Timer()
	result = list(counter)

	# TODO Sort before each loop?
	# TODO Prevent more than 1% chained combination steps, probably.
	# TODO Speed up.
	diff_times = list()
	cmp_times = list()
	for smaller in reversed(result):
		cmp_timer = Timer()
		diff = 1
		diff_item = None
		t = result[:result.index(smaller)]

		if len(result) == 1:
			break

		for larger in reversed(t):
			diff_timer = Timer()
			ndiff = diff_colors(smaller[0], larger[0])
			diff_times.append(diff_timer.elapsed())
			if ndiff <= diff:
				diff = ndiff
				diff_item = larger

		if diff < 0.1:
			diff_item[1] = diff_item[1] + smaller[1]
			result.remove(smaller)
		cmp_times.append(cmp_timer.elapsed())

	print("\n[COMPRESS]")
	print("Colors: {}".format(len(result)))
	print("Diff time: {} seconds, {} times".format(sum(diff_times), len(diff_times)))
	print("Diff avg. time: {} milliseconds".format(sum(diff_times) * 1000 / len(diff_times)))
	print("Cmp time: {} seconds, {} times".format(sum(cmp_times), len(cmp_times)))
	print("Cmp avg. time: {} milliseconds".format(sum(cmp_times) * 1000 / len(cmp_times)))
	print("Time: {} seconds".format(timer.elapsed()))

	return result


def diff_colors(c1, c2):
	# TODO Fail faster.
	hue = abs((c2[0] - c1[0]) / 255)
	saturation = abs((c2[1] - c1[1]) / 255)
	value = abs((c2[2] - c1[2]) / 255)
	return (hue + saturation + value) / 3


def print_result(counter, total):
	print("\n[RESULT]")
	for key, value in counter:
		print("{0:15}:{1:>7}% ({2})".format(str(key), "{0:.2f}".format(value / total * 100), value))


def image_result(counter, size, path):
	result = Image.new("HSV", (len(counter) * size, size), (0, 0, 0, 0))
	canvas = ImageDraw.Draw(result)
	for idx, item in enumerate(counter):
		canvas.rectangle([(idx * size, 0), ((idx * size) + (size - 1), (size - 1))], fill=item[0])

	file_name = os.path.splitext(os.path.basename(path))[0]
	file_name = "{0} {1}.png".format(file_name, time.strftime("%Y-%m-%d %H%M%S", time.localtime()))
	result = result.convert("RGBA")
	result.save(os.path.join("results", file_name), "PNG")


def main():
	timer = Timer()
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
	counter = compress(counter)

	# wanted = min(10, len(counter))
	# counter = counter[:wanted]

	counter = sorted(counter, key=lambda x: x[1], reverse=True)
	print_result(counter, len(pixels))
	image_result(counter, 150, path)
	print("\nTotal time: {} seconds".format(timer.elapsed()))


if __name__ == "__main__":
	main()
