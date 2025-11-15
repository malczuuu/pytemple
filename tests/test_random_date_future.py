import random
from datetime import date, timedelta

import pytest

import pytemple


@pytest.mark.repeat(10)
def test_date_future_within_days():
    random.seed(0)
    result = pytemple.loads("${random.date.future(days=7)}")
    d = date.fromisoformat(result)
    now = date.today()
    assert now <= d <= now + timedelta(days=7)


def test_date_future_within_negative_days_not_resolving():
    src = "${random.date.future(days=-7)}"
    result = pytemple.loads(src)

    assert result == src
