import string

import pytest

import pytemple


@pytest.mark.repeat(10)
def test_string_length_and_charset():
    result = pytemple.loads("${random.string(10)}")

    assert len(result) == 10
    assert all(c in string.ascii_lowercase for c in result)


@pytest.mark.repeat(10)
def test_string_zero_length():
    result = pytemple.loads("${random.string(0)}")

    assert result == ""


@pytest.mark.repeat(10)
def test_string_negative_not_replaced():
    src = "${random.string(-1)}"

    assert pytemple.loads(src) == src


@pytest.mark.repeat(10)
def test_string_large_length():
    result = pytemple.loads("${random.string(1000)}")

    assert len(result) == 1000
    assert all("a" <= c <= "z" for c in result)
