import pytest
import pygame
from paterdal import Paterdal


def test_instance_is_correct():
    """
    Verifies that a Paterdal instance initializes correctly
    :return:
    """
    p = Paterdal()
    assert p.col_offset == 10
    assert p.row_offset == 10
    assert p.h_tile_size == 80
    assert p.v_tile_size == 80
    assert p.line_width == 4
    assert p.line_color == (0, 0, 0)
    assert p.back_color == (255, 255, 255)
    assert p.cols == 5
    assert p.rows == 6


def test_get_size():
    p = Paterdal()
    c, r = p.get_size()
    assert c, r == (420, 500)

