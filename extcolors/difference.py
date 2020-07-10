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
    l = c2[0] - c1[0]
    a = c2[1] - c1[1]
    b = c2[2] - c1[2]
    return math.sqrt((l * l) + (a * a) + (b * b))
