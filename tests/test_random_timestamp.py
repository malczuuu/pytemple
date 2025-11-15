import time

import pytest

import pytemple


@pytest.mark.repeat(10)
def test_timestamp_is_integer_and_recent():
    result = pytemple.loads("${random.timestamp}")

    ts = int(result)
    now = int(time.time())
    assert abs(now - ts) < 5, "should be within a few seconds"
