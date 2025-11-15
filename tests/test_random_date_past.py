import random
from datetime import date, timedelta

import pytest

import pytemple


@pytest.mark.repeat(10)
def test_date_past_within_days():
    random.seed(0)
    result = pytemple.loads("${random.date.past(days=30)}")
    d = date.fromisoformat(result)
    now = date.today()
    assert now - timedelta(days=30) <= d <= now


def test_date_past_within_negative_days_not_resolving():
    src = "${random.date.past(days=-30)}"
    result = pytemple.loads(src)

    assert result == src
