import pytest
from module_math import add, subtract, divide


def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5


def test_divide():
    assert divide(6, 2) == 3
    with pytest.raises(ValueError):
        divide(1, 0)
