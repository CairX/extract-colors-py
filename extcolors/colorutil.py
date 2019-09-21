# coding: utf8

import math


def cie76(c1, c2):
	"""
	Color comparision using CIE76 algorithm.
	Returns a value between 0 and 100.
	Where 0 is a perfect match and 100 is opposing colors.
	http://zschuessler.github.io/DeltaE/learn/

	LAB Delta E - version CIE76
	https://en.wikipedia.org/wiki/Color_difference

	E* = 2.3 corresponds to a JND (just noticeable difference)
	"""
	return math.sqrt(
		math.pow(c2[0] - c1[0], 2) +
		math.pow(c2[1] - c1[1], 2) +
		math.pow(c2[2] - c1[2], 2)
	)


def rgb_xyz(rgb):
	"""
	Convert tuple from the sRGB color space to the CIE XYZ color space.

	The XYZ output is determined using D65 illuminate with a 2° observer angle.
	https://en.wikipedia.org/wiki/Illuminant_D65

	sRGB (standard Red Green Blue): https://en.wikipedia.org/wiki/SRGB
	CIE XYZ: https://en.wikipedia.org/wiki/CIE_1931_color_space
	"""
	r = rgb[0] / 255.0
	g = rgb[1] / 255.0
	b = rgb[2] / 255.0

	x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
	y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
	z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

	x = x * 100.0
	y = y * 100.0
	z = z * 100.0

	return x, y, z


def xyz_rgb(xyz):
	"""
	Convert tuple from the CIE XYZ color space to the sRGB color space.

	Conversion is based on that the XYZ input uses an the D65 illuminate with a 2° observer angle.
	https://en.wikipedia.org/wiki/Illuminant_D65

	sRGB (standard Red Green Blue): https://en.wikipedia.org/wiki/SRGB
	CIE XYZ: https://en.wikipedia.org/wiki/CIE_1931_color_space
	"""
	x = xyz[0] / 100.0
	y = xyz[1] / 100.0
	z = xyz[2] / 100.0

	r = x *  3.2404542 + y * -1.5371385 + z * -0.4985314
	g = x * -0.9692660 + y *  1.8760108 + z *  0.0415560
	b = x *  0.0556434 + y * -0.2040259 + z *  1.0572252

	r = r * 255.0
	g = g * 255.0
	b = b * 255.0

	return round(r), round(g), round(b)


def xyz_lab(xyz):
	"""
	Convert tuple from the CIE XYZ color space to the CIE L*a*b color space.

	Conversion is based on that the XYZ input uses an the D65 illuminate with a 2° observer angle.
	https://en.wikipedia.org/wiki/Illuminant_D65

	CIE L*a*b: https://en.wikipedia.org/wiki/Lab_color_space
	CIE XYZ: https://en.wikipedia.org/wiki/CIE_1931_color_space
	"""
	x = __pivot_xyz_lab(xyz[0] / 95.047)
	y = __pivot_xyz_lab(xyz[1] / 100.000)
	z = __pivot_xyz_lab(xyz[2] / 108.883)

	l = max(0.0, (116.0 * y) - 16.0)
	a = 500.0 * (x - y)
	b = 200.0 * (y - z)

	return l, a, b


def __pivot_xyz_lab(value):
	if value > 0.008856:
		value = math.pow(value, 1.0 / 3.0)
	else:
		value = (value * 7.787) + (16.0 / 116.0)
	return value


def lab_xyz(lab):
	"""
	Convert tuple from the CIE L*a*b* color space to the CIE XYZ color space.

	The XYZ output is determined using D65 illuminate with a 2° observer angle.
	https://en.wikipedia.org/wiki/Illuminant_D65

	CIE L*a*b: https://en.wikipedia.org/wiki/Lab_color_space
	CIE XYZ: https://en.wikipedia.org/wiki/CIE_1931_color_space
	"""
	y = (lab[0] + 16.0) / 116.0
	x = lab[1] / 500.0 + y
	z = y - lab[2] / 200.0

	x = __pivot_lab_xyz(x) * 95.047
	y = __pivot_lab_xyz(y) * 100.000
	z = __pivot_lab_xyz(z) * 108.883

	return x, y, z


def __pivot_lab_xyz(value):
	if value > 0.008856:
		value = math.pow(value, 3)
	else:
		value = (value - 16.0 / 116.0) / 7.787
	return value


def rgb_lab(rgb):
	"""
	Convert tuple from the sRGB color space to the CIE L*a*b* color space.
	Shorthand method for chaining sRGB => CIE XYZ => CIE L*a*b*.
	"""
	return xyz_lab(rgb_xyz(rgb))


def lab_rgb(lab):
	"""
	Convert tuple from the CIE L*a*b* color space to the sRGB color space.
	Shorthand method for chaining CIE L*a*b* => CIE XYZ  => sRGB.
	"""
	return xyz_rgb(lab_xyz(lab))
