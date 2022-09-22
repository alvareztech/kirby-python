import pytest

from main import checkFloat


def test_checkFloat():
    assert checkFloat('8') == 8
