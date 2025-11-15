import pytest

import pytemple


@pytest.mark.repeat(10)
def test_int_positive_range():
    result = pytemple.loads("${random.int(0, 30)}")
    val = int(result)
    assert 0 <= val <= 30


@pytest.mark.repeat(10)
def test_int_negative_range():
    result = pytemple.loads("${random.int(-10, -1)}")

    val = int(result)

    assert -10 <= val <= -1


@pytest.mark.repeat(10)
def test_int_range():
    result = pytemple.loads("${random.int(-10, 10)}")

    val = int(result)

    assert -10 <= val <= 10


@pytest.mark.repeat(10)
def test_int_equal_bounds():
    result = pytemple.loads("${random.int(5, 5)}")

    assert result == "5"


@pytest.mark.repeat(10)
def test_int_reversed_bounds_raises():
    with pytest.raises(ValueError):
        pytemple.loads("${random.int(10, 5)}")


@pytest.mark.repeat(10)
def test_int_non_integer_args_not_replaced():
    src = "${random.int(0.5, 3.2)}"

    assert pytemple.loads(src) == src
