import math


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


def rgb_xyz(rgb):
	""" sRGB - standard RGB """
	r = pivot_rgb_xyz(rgb[0] / 255)
	g = pivot_rgb_xyz(rgb[1] / 255)
	b = pivot_rgb_xyz(rgb[2] / 255)

	# x, y and z output refer to a D65/2° standard illuminant
	# Illuminant = D65, Observer = 2°
	x = r * 0.4124 + g * 0.3576 + b * 0.1805
	y = r * 0.2126 + g * 0.7152 + b * 0.0722
	z = r * 0.0193 + g * 0.1192 + b * 0.9505

	return x, y, z


def pivot_rgb_xyz(value):
	""" sRGB - standard RGB """
	if value > 0.04045:
		value = math.pow((value + 0.055) / 1.055, 2.4)
	else:
		value /= 12.92
	return value * 100


def xyz_rgb(xyz):
	""" sRGB - standard RGB """
	x = xyz[0] / 100
	y = xyz[1] / 100
	z = xyz[2] / 100

	r = x * 3.2406 + y * -1.5372 + z * -0.4986
	g = x * -0.9689 + y * 1.8758 + z * 0.0415
	b = x * 0.0557 + y * -0.2040 + z * 1.0570

	r = pivot_xyz_rgb(r) * 255
	g = pivot_xyz_rgb(g) * 255
	b = pivot_xyz_rgb(b) * 255

	return r, g, b


def pivot_xyz_rgb(value):
	""" sRGB - standard RGB """
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


def rgb_lab(rgb):
	return xyz_lab(rgb_xyz(rgb))


def lab_rgb(lab):
	return rgb_xyz(lab_xyz(lab))
