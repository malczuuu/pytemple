from datetime import date, datetime

import pytest

import pytemple


@pytest.mark.repeat(10)
def test_date_with_iso_range_unquoted():
    result = pytemple.loads("${random.date(2020-01-01, 2020-01-10)}")

    d = date.fromisoformat(result)
    assert date(2020, 1, 1) <= d <= date(2020, 1, 10)


@pytest.mark.repeat(10)
def test_date_with_iso_range_single_quoted():
    result = pytemple.loads("${random.date('2020-01-01', '2020-01-10')}")

    d = date.fromisoformat(result)
    assert date(2020, 1, 1) <= d <= date(2020, 1, 10)


@pytest.mark.repeat(10)
def test_date_with_iso_range_single_quoted_one():
    result = pytemple.loads("${random.date('2020-01-01', 2020-01-10)}")

    d = date.fromisoformat(result)
    assert date(2020, 1, 1) <= d <= date(2020, 1, 10)


@pytest.mark.repeat(10)
def test_date_with_iso_range_double_unquoted():
    result = pytemple.loads('${random.date("2020-01-01", "2020-01-10")}')

    d = date.fromisoformat(result)
    assert date(2020, 1, 1) <= d <= date(2020, 1, 10)


@pytest.mark.repeat(10)
def test_date_with_iso_range_double_unquoted_one():
    result = pytemple.loads('${random.date(2020-01-01, "2020-01-10")}')

    d = date.fromisoformat(result)
    assert date(2020, 1, 1) <= d <= date(2020, 1, 10)


@pytest.mark.repeat(10)
def test_date_with_quoted_args_and_epoch():
    # epoch for 2020-01-01 and 2020-01-03 using datetime.timestamp()
    start_timestamp = str(int(datetime(2020, 1, 1).timestamp()))
    end_timestamp = str(int(datetime(2020, 1, 3).timestamp()))

    src = '${random.date("' + start_timestamp + '", "' + end_timestamp + '")}'
    result = pytemple.loads(src)

    d = date.fromisoformat(result)
    assert date(2020, 1, 1) <= d <= date(2020, 1, 3)


def test_date_invalid_not_replaced():
    src = "${random.date(2020-01-10, 2020-01-01)}"
    assert pytemple.loads(src) == src


def test_date_invalid_format_not_replaced():
    src = "${random.date(invalid, format)}"
    assert pytemple.loads(src) == src
