from extcolors import difference


CIE76_SETS = (
    # White - Black
    ((100, 0, 0), (  0, 0, 0), 100),
    ((  0, 0, 0), (100, 0, 0), 100),

    # Solarized color palette
    # Base03 - Base02
    ((15, -12, -12), (20, -12, -12), 5),
    ((20, -12, -12), (15, -12, -12), 5),
    # Base0 - Base1
    ((60, -6, -3), (65, -5, -2), 5.1962),
    ((65, -5, -2), (60, -6, -3), 5.1962),
    # Base2 - Base3
    ((92, -0, 10), (97,  0, 10), 5),
    ((97,  0, 10), (92, -0, 10), 5),
    # Base03 - Green
    ((15, -12, -12), (60, -20,  65), 89.5433),
    ((60, -20,  65), (15, -12, -12), 89.5433),
    # Yellow - Orange
    ((60,   10,  65), (50, 50, 55), 42.4264),
    ((50, 50, 55), (60,   10,  65), 42.4264),
    # Magenta - Blue
    ((50,  65,  -5), (55, -10, -45), 85.1469),
    ((55, -10, -45), (50,  65,  -5), 85.1469),
    # Red - Cyan
    ((50,  65, 45), (60, -35, -5), 112.2497),
    ((60, -35, -5), (50,  65, 45), 112.2497),
) # yapf: disable


def within_tolerance(value, expected):
    return abs(value - expected) <= 0.0001


def test_difference_cie76():
    for a, b, expected_delta in CIE76_SETS:
        delta = difference.cie76(a, b)
        assert within_tolerance(delta, expected_delta)
