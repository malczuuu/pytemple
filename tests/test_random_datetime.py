from datetime import datetime

import pytest

import pytemple


@pytest.mark.repeat(10)
def test_datetime_iso_range_unquoted():
    result = pytemple.loads("${random.datetime(2020-01-01T00:00:00, 2020-01-02T00:00:00)}")
    dt = datetime.fromisoformat(result)
    assert datetime(2020, 1, 1) <= dt <= datetime(2020, 1, 2)


@pytest.mark.repeat(10)
def test_datetime_iso_range_single_quoted():
    result = pytemple.loads("${random.datetime('2020-01-01T00:00:00', '2020-01-02T00:00:00')}")
    dt = datetime.fromisoformat(result)
    assert datetime(2020, 1, 1) <= dt <= datetime(2020, 1, 2)


@pytest.mark.repeat(10)
def test_datetime_iso_range_single_quoted_one():
    result = pytemple.loads("${random.datetime('2020-01-01T00:00:00', 2020-01-02T00:00:00)}")
    dt = datetime.fromisoformat(result)
    assert datetime(2020, 1, 1) <= dt <= datetime(2020, 1, 2)


@pytest.mark.repeat(10)
def test_datetime_iso_range_double_quoted():
    result = pytemple.loads('${random.datetime("2020-01-01T00:00:00", "2020-01-02T00:00:00")}')
    dt = datetime.fromisoformat(result)
    assert datetime(2020, 1, 1) <= dt <= datetime(2020, 1, 2)


@pytest.mark.repeat(10)
def test_datetime_iso_range_double_quoted_one():
    result = pytemple.loads('${random.datetime(2020-01-01T00:00:00, "2020-01-02T00:00:00")}')
    dt = datetime.fromisoformat(result)
    assert datetime(2020, 1, 1) <= dt <= datetime(2020, 1, 2)


@pytest.mark.repeat(10)
def test_datetime_with_quotes_and_epoch():
    start_timestamp = str(int(datetime(2020, 1, 1, 0, 0).timestamp()))
    end_timestamp = str(int(datetime(2020, 1, 1, 2, 0).timestamp()))

    src = '${random.datetime("' + start_timestamp + '", "' + end_timestamp + '")}'
    result = pytemple.loads(src)

    dt = datetime.fromisoformat(result)
    assert datetime(2020, 1, 1, 0, 0) <= dt <= datetime(2020, 1, 1, 2, 0)


def test_datetime_invalid_range_not_replaced():
    src = "${random.datetime(2020-01-02T00:00:00, 2020-01-01T00:00:00)}"
    assert pytemple.loads(src) == src


def test_datetime_invalid_range_format_not_replaced():
    src = "${random.datetime(invalid, format)}"
    assert pytemple.loads(src) == src
