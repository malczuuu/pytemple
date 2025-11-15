import pytest

import pytemple


@pytest.mark.repeat(10)
def test_double_range():
    result = pytemple.loads("${random.double(0.5, 2.5)}")
    val = float(result)

    assert 0.5 <= val <= 2.5


@pytest.mark.repeat(10)
def test_double_equal_bounds():
    result = pytemple.loads("${random.double(1.23, 1.23)}")

    assert abs(float(result) - 1.23) < 1e-9


@pytest.mark.repeat(10)
def test_double_invalid_format_not_replaced():
    src = "${random.double(.5, 1)}"

    assert pytemple.loads(src) == src
