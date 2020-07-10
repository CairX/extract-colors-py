# coding: utf8

from extcolors import conversion

COLOR_SETS = (
    # In the color sets a four point precision is used in order to get accurate conversion
    # from xyz and lab to other formats as the result will vary in quite a wide range based
    # on precision.
    #
    # For the white, grey, and black test colors the RGB space has been used as the base in
    # order to establish the values for the other color spaces. For the Solarized palette
    # the CIE L*a*b* spaces was used as the base.
    #
    # Order of formats: RGB, CIE XYZ, CIE L*a*b*

    # White / Grey / Black
    ((255, 255, 255), (95.0470, 100.0000, 108.8830), (100.0000, 0, 0)),
    ((254, 254, 254), (94.2013,  99.1102, 107.9142), ( 99.6549, 0, 0)),
    ((230, 230, 230), (75.2105,  79.1298,  86.1589), ( 91.2930, 0, 0)),
    ((204, 204, 204), (57.3920,  60.3827,  65.7465), ( 82.0458, 0, 0)),
    ((179, 179, 179), (42.8458,  45.0786,  49.0829), ( 72.9436, 0, 0)),
    ((153, 153, 153), (30.2769,  31.8547,  34.6843), ( 63.2226, 0, 0)),
    ((128, 128, 128), (20.5169,  21.5861,  23.5035), ( 53.5850, 0, 0)),
    ((102, 102, 102), (12.6287,  13.2868,  14.4671), ( 43.1923, 0, 0)),
    (( 77,  77,  77), ( 7.0538,   7.4214,   8.0806), ( 32.7475, 0, 0)),
    (( 51,  51,  51), ( 3.1465,   3.3105,   3.6045), ( 21.2467, 0, 0)),
    (( 26,  26,  26), ( 0.9818,   1.0330,   1.1247), (  9.2632, 0, 0)),
    ((  1,   1,   1), ( 0.0288,   0.0304,   0.0330), (  0.2742, 0, 0)),
    ((  0,   0,   0), (      0,        0,        0), (       0, 0, 0)),

    # Solarized color palette
    (( -13.2900,  42.9751,  54.2432), ( 1.3679,  1.9086,  3.8156), (15, -12, -12)),
    ((  -3.9725,  53.8878,  65.4680), ( 2.2315,  2.9891,  5.5307), (20, -12, -12)),
    ((  86.3116, 110.4335, 117.8033), (12.7467, 14.5417, 19.2100), (45,  -7,  -7)),
    ((  98.6033, 122.9919, 130.4939), (16.2456, 18.4187, 23.9881), (50,  -7,  -7)),
    (( 130.1478, 147.9923, 149.5942), (25.2884, 28.1233, 32.7733), (60,  -6,  -3)),
    (( 146.1312, 160.5956, 161.0797), (30.9903, 34.0472, 38.6872), (65,  -5,  -2)),
    (( 240.3075, 231.3023, 212.9823), (76.7071, 80.7044, 74.4627), (92,  -0,  10)),
    (( 254.7499, 245.6123, 227.0867), (87.8617, 92.4403, 85.9351), (97,   0,  10)),
    (( 186.8636, 135.8671,   1.0947), (29.2538, 28.1233,  3.9191), (60,  10,  65)),
    (( 207.1744,  75.2769,  20.9957), (28.4544, 18.4187,  2.7660), (50,  50,  55)),
    (( 224.1507,  50.7372,  46.0058), (32.4568, 18.4187,  4.4310), (50,  65,  45)),
    (( 211.5000,  56.6440, 129.5884), (32.4570, 18.4187, 22.8162), (50,  65,  -5)),
    ((  92.0049, 114.6157, 195.6700), (20.4241, 18.4187, 54.4960), (50,  15, -45)),
    ((-104.1110, 140.7924, 209.2569), (19.7267, 22.9298, 63.8622), (55, -10, -45)),
    ((  31.4784, 161.1706, 152.3212), (19.0454, 28.1233, 34.2623), (60, -35,  -5)),
    (( 140.7182, 152.1682, -11.9700), (22.1270, 28.1233,  3.9191), (60, -20,  65)),
) # yapf: disable



def within_tolerance(value, expected):
    """
    Verify that all values of the color tuple are within a range of tolerance.
    """
    t = 0.01
    return ((expected[0] - t) <= value[0] <= (expected[0] + t)
            and (expected[1] - t) <= value[1] <= (expected[1] + t)
            and (expected[2] - t) <= value[2] <= (expected[2] + t))


def test_conversion_rgb_to_xyz():
    for rgb, xyz, _ in COLOR_SETS:
        converted = conversion.rgb_xyz(rgb)
        assert within_tolerance(converted, xyz)


def test_conversion_xyz_to_rgb():
    for rgb, xyz, _ in COLOR_SETS:
        converted = conversion.xyz_rgb(xyz)
        assert within_tolerance(converted, rgb)


def test_conversion_xyz_to_lab():
    for _, xyz, lab in COLOR_SETS:
        converted = conversion.xyz_lab(xyz)
        assert within_tolerance(converted, lab)


def test_conversion_lab_to_xyz():
    for _, xyz, lab in COLOR_SETS:
        converted = conversion.lab_xyz(lab)
        assert within_tolerance(converted, xyz)


def test_conversion_rgb_to_lab():
    for rgb, _, lab in COLOR_SETS:
        converted = conversion.rgb_lab(rgb)
        assert within_tolerance(converted, lab)


def test_conversion_lab_to_rgb():
    for rgb, _, lab in COLOR_SETS:
        converted = conversion.lab_rgb(lab)
        assert within_tolerance(converted, rgb)
