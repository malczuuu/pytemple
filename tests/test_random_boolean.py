import pytest

import pytemple


@pytest.mark.repeat(10)
def test_boolean_single_and_values():
    result = pytemple.loads("${random.boolean}")

    assert result in ("true", "false")


@pytest.mark.repeat(10)
def test_boolean_multiple():
    result = pytemple.loads("${random.boolean},${random.boolean},${random.boolean}")
    parts = result.split(",")

    assert len(parts) == 3
    assert all(p in ("true", "false") for p in parts)
