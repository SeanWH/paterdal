from paterdal import Paterdal


def test_instance_is_correct():
    """
    Verifies that a Paterdal instance initializes correctly
    :return:
    """

    class ExpectedData:
        def __init__(self):
            self.col_offset = 10
            self.row_offset = 10
            self.h_tile_size = 80
            self.v_tile_size = 80
            self.line_width = 4
            self.line_color = (0, 0, 0)
            self.back_color = (255, 255, 255)
            self.cols = 5
            self.rows = 6

    actual = Paterdal()
    expected = ExpectedData()

    assert expected.col_offset == actual.col_offset
    assert expected.row_offset == actual.row_offset
    assert expected.h_tile_size == actual.h_tile_size
    assert expected.v_tile_size == actual.v_tile_size
    assert expected.line_width == actual.line_width
    assert expected.line_color == actual.line_color
    assert expected.back_color == actual.back_color
    assert expected.cols == actual.cols
    assert expected.rows == actual.rows


def test_calculate_points_col_0_row_0():
    p = Paterdal()
    expected = [
        (10, 10),
        (90, 10),
        (90, 90),
        (10, 90)
    ]

    actual = p.calculate_points(0, 0)
    assert expected == actual


def test_get_size_with_all_defaults():
    """
    This tests get_size with all it's default values.
    :return:
    """
    p = Paterdal()
    expected = (420, 500)
    actual = p.get_size()
    assert expected == actual


def test_calculate_new_size_200x300():
    """
    This tests function with min possible
    screen size.  Note: also covers get_test
    as well.
    :return:
    """
    p = Paterdal()
    expected = (250, 300)
    actual = p.calculate_new_size(200, 300)
    assert expected == actual


def test_calculate_new_size_2560x1009():
    """
    Tests calculate_new_size
    :return:
    """
    p = Paterdal()
    expected = (2560, 2966)
    actual = p.calculate_new_size(2560, 1009)
    assert expected == actual
