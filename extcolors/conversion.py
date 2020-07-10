# coding: utf8

import math


def rgb_xyz(rgb):
    """
    Convert tuple from the sRGB color space to the CIE XYZ color space.

    The XYZ output is determined using D65 illuminate with a 2° observer angle.
    https://en.wikipedia.org/wiki/Illuminant_D65

    The conversion matrix used was provided by Bruce Lindbloom:
    http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html

    Formulas for conversion:
    http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    https://easyrgb.com/en/math.php

    Information about respective color space:
    sRGB (standard Red Green Blue): https://en.wikipedia.org/wiki/SRGB
    CIE XYZ: https://en.wikipedia.org/wiki/CIE_1931_color_space
    """
    r = rgb[0] / 255.0
    g = rgb[1] / 255.0
    b = rgb[2] / 255.0

    r = _pivot_rgb_xyz(r)
    g = _pivot_rgb_xyz(g)
    b = _pivot_rgb_xyz(b)

    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    x = x * 100.0
    y = y * 100.0
    z = z * 100.0

    return x, y, z


def _pivot_rgb_xyz(value):
    if value <= 0.04045:
        value = value / 12.92
    else:
        value = math.pow((value + 0.055) / 1.055, 2.4)
    return value


def xyz_rgb(xyz):
    """
    Convert tuple from the CIE XYZ color space to the sRGB color space.

    Conversion is based on that the XYZ input uses an the D65 illuminate with a 2° observer angle.
    https://en.wikipedia.org/wiki/Illuminant_D65

    The inverse conversion matrix used was provided by Bruce Lindbloom:
    http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html

    Formulas for conversion:
    http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    https://easyrgb.com/en/math.php

    Information about respective color space:
    sRGB (standard Red Green Blue): https://en.wikipedia.org/wiki/SRGB
    CIE XYZ: https://en.wikipedia.org/wiki/CIE_1931_color_space
    """
    x = xyz[0] / 100.0
    y = xyz[1] / 100.0
    z = xyz[2] / 100.0

    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252

    r = _pivot_xyz_rgb(r)
    g = _pivot_xyz_rgb(g)
    b = _pivot_xyz_rgb(b)

    r = r * 255.0
    g = g * 255.0
    b = b * 255.0

    return r, g, b


def _pivot_xyz_rgb(value):
    if value <= 0.0031308:
        value = value * 12.92
    else:
        value = (math.pow(value, 0.4166666) * 1.055) - 0.055
    return value


def xyz_lab(xyz):
    """
    Convert tuple from the CIE XYZ color space to the CIE L*a*b color space.

    Conversion is based on that the XYZ input uses an the D65 illuminate with a 2° observer angle.
    https://en.wikipedia.org/wiki/Illuminant_D65

    Formulas for conversion:
    https://en.wikipedia.org/wiki/CIELAB_color_space#CIELAB%E2%80%93CIEXYZ_conversions
    http://www.brucelindbloom.com/index.html?Eqn_XYZ_to_Lab.html
    https://easyrgb.com/en/math.php

    Information about respective color space:
    CIE L*a*b: https://en.wikipedia.org/wiki/Lab_color_space
    CIE XYZ: https://en.wikipedia.org/wiki/CIE_1931_color_space
    """
    x = xyz[0] / 95.047
    y = xyz[1] / 100.000
    z = xyz[2] / 108.883

    x = _pivot_xyz_lab(x)
    y = _pivot_xyz_lab(y)
    z = _pivot_xyz_lab(z)

    l = max(0.0, (116.0 * y) - 16.0)
    a = (x - y) * 500.0
    b = (y - z) * 200.0

    return l, a, b


def _pivot_xyz_lab(value):
    if value > 0.008856:
        value = math.pow(value, 0.3333333)
    else:
        value = ((value * 903.3) + 16.0) / 116.0
    return value


def lab_xyz(lab):
    """
    Convert tuple from the CIE L*a*b* color space to the CIE XYZ color space.

    The XYZ output is determined using D65 illuminate with a 2° observer angle.
    https://en.wikipedia.org/wiki/Illuminant_D65

    Formulas for conversion:
    https://en.wikipedia.org/wiki/CIELAB_color_space#CIELAB%E2%80%93CIEXYZ_conversions
    http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    https://easyrgb.com/en/math.php

    Information about respective color space:
    CIE L*a*b: https://en.wikipedia.org/wiki/Lab_color_space
    CIE XYZ: https://en.wikipedia.org/wiki/CIE_1931_color_space
    """
    l = lab[0]
    a = lab[1]
    b = lab[2]

    # Reminder: The y values is calculated first as it can be reused
    # for the calculation of x and z.
    y = (l + 16.0) / 116.0
    x = y + (a / 500.0)
    z = y - (b / 200.0)

    x3 = x * x * x
    z3 = z * z * z

    x = x3 if x3 > 0.008856 else ((x * 116.0) - 16.0) / 903.3
    y = (y * y * y) if l > 7.9996248 else l / 903.3
    z = z3 if z3 > 0.008856 else ((z * 116.0) - 16.0) / 903.3

    x = x * 95.047
    y = y * 100.000
    z = z * 108.883

    return x, y, z


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
