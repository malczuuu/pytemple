import re

import pytest

import pytemple

UUID_REGEXP = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


@pytest.mark.repeat(10)
def test_uuid_format_and_multiple():
    result = pytemple.loads("${random.uuid} ${random.uuid}")

    parts = result.split()

    assert len(parts) == 2
    assert UUID_REGEXP.match(parts[0])
    assert UUID_REGEXP.match(parts[1])
    assert parts[0] != parts[1]
