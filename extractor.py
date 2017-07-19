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


def srgb_xyz(rgb):
	r = pivot_srgb_xyz(rgb[0] / 255)
	g = pivot_srgb_xyz(rgb[1] / 255)
	b = pivot_srgb_xyz(rgb[2] / 255)

	# x, y and z output refer to a D65/2° standard illuminant
	# Illuminant = D65, Observer = 2°
	x = r * 0.4124 + g * 0.3576 + b * 0.1805
	y = r * 0.2126 + g * 0.7152 + b * 0.0722
	z = r * 0.0193 + g * 0.1192 + b * 0.9505

	return x, y, z


def pivot_srgb_xyz(value):
	if value > 0.04045:
		value = math.pow((value + 0.055) / 1.055, 2.4)
	else:
		value /= 12.92
	return value * 100


def xyz_srgb(xyz):
	x = xyz[0] / 100
	y = xyz[1] / 100
	z = xyz[2] / 100

	r = x * 3.2406 + y * -1.5372 + z * -0.4986
	g = x * -0.9689 + y * 1.8758 + z * 0.0415
	b = x * 0.0557 + y * -0.2040 + z * 1.0570

	r = pivot_xyz_srgb(r) * 255
	g = pivot_xyz_srgb(g) * 255
	b = pivot_xyz_srgb(b) * 255

	return r, g, b

def pivot_xyz_srgb(value):
	if value > 0.0031308:
		value = 1.055 * math.pow(value, (1 / 2.4)) - 0.055
	else:
		value = 12.92 * value
	return value


def xyz_lab(xyz):
	# Illuminant = D65
	x = pivot_xyz_lab(xyz[0] / 95.047)
	y = pivot_xyz_lab(xyz[1] / 100.000)
	z = pivot_xyz_lab(xyz[2] / 108.883)

	l = max(0.0, (116 * y) - 16)
	a = 500 * (x - y)
	b = 200 * (y - z)

	return l, a, b


def pivot_xyz_lab(value):
	if value > 0.008856:
		value = math.pow(value, 1 / 3)
	else:
		value = (value * 7.787) + (16 / 116)
	return value


def lab_xyz(lab):
	y = (lab[0] + 16) / 116
	x = lab[1] / 500 + y
	z = y - lab[2] / 200

	# Illuminant = D65
	x = pivot_lab_xyz(x) * 95.047
	y = pivot_lab_xyz(y) * 100.000
	z = pivot_lab_xyz(z) * 108.883

	return x, y, z


def pivot_lab_xyz(value):
	if value > 0.008856:
		value = math.pow(value, 3)
	else:
		value = (value - 16 / 116) / 7.787
	return value


def count_colors(pixels):
	timer = Timer()
	counter = defaultdict(int)
	for color in pixels:
		counter[color] += 1

	print("\n[COUNTER]")
	print("Colors: {}".format(len(counter)))
	print("Time: {} seconds".format(timer.elapsed()))

	return counter


def compress(counter):
	timer = Timer()
	result = counter

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
			ndiff = cie76(smaller1, larger)
			diff_times.append(diff_timer.elapsed())

			# http://zschuessler.github.io/DeltaE/learn/
			if ndiff < 12.2:
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


def cie76(c1, c2):
	"""
	LAB Delta E - version CIE76
	https://en.wikipedia.org/wiki/Color_difference

	E* ≈ 2.3 corresponds to a JND (just noticeable difference)
	"""
	return math.sqrt(
		math.pow(c2[0] - c1[0], 2) +
		math.pow(c2[1] - c1[1], 2) +
		math.pow(c2[2] - c1[2], 2)
	)


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
	columns = 5
	width = min(len(counter), columns) * size
	height = (math.floor(len(counter) / columns) + 1) * size

	result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
	canvas = ImageDraw.Draw(result)
	for idx, item in enumerate(counter):
		color = round(item[0][0]), round(item[0][1]), round(item[0][2])
		x = (idx % columns) * size
		y = math.floor(idx / columns) * size
		w = size - 1
		h = size - 1
		canvas.rectangle([(x, y), (x + w, y + h)], fill=color)

	file_name = os.path.splitext(os.path.basename(path))[0]
	file_name = "{0} {1}.png".format(file_name, time.strftime("%Y-%m-%d %H%M%S", time.localtime()))
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
	tmp = dict()
	for color, count in counter.items():
		tmp[xyz_lab(srgb_xyz(color))] = count

	counter = compress(tmp)

	# wanted = min(10, len(counter))
	# counter = counter[:wanted]

	counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
	counter = [(xyz_srgb(lab_xyz(c[0])), c[1]) for c in counter]
	print_result(counter, len(pixels))
	image_result(counter, 150, path)
	print("\nTotal time: {} seconds".format(timer.elapsed()))


if __name__ == "__main__":
	main()
