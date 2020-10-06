import os

import extcolors


def _get_data_path(relative_data_path):
    data_path = os.path.realpath(__file__)
    data_path = os.path.dirname(data_path)
    data_path = os.path.join(data_path, "data")
    return os.path.join(data_path, relative_data_path)


def test_extraction_black_with_transparency():
    data_path = _get_data_path("16x16_8x8_black_square_transparent_border.png")
    colors, pixel_count = extcolors.extract_from_path(data_path)
    expected = [((0, 0, 0), 64)]
    assert colors == expected


def test_extraction_white_with_transparency():
    data_path = _get_data_path("16x16_8x8_white_square_transparent_border.png")
    colors, pixel_count = extcolors.extract_from_path(data_path)
    expected = [((255, 255, 255), 64)]
    assert colors == expected
