import math


def cie76(c1, c2):
    """
    Color comparision using CIE76 algorithm.
    Returns a float value where 0 is a perfect match and 100 is
    opposing colors. Note that the range can be larger than 100.
    http://zschuessler.github.io/DeltaE/learn/

    LAB Delta E - version CIE76
    https://en.wikipedia.org/wiki/Color_difference

    E* = 2.3 corresponds to a JND (just noticeable difference)
    """
    l = c2[0] - c1[0]
    a = c2[1] - c1[1]
    b = c2[2] - c1[2]
    return math.sqrt((l * l) + (a * a) + (b * b))
