import os
import re
import tempfile
import time
from datetime import datetime, date, timedelta
from typing import Generator

import pytest

import pytemple


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    tf = tempfile.NamedTemporaryFile(mode="w", delete=False)
    tf.write("value=${random.int(10, 20)}")
    tf.close()

    yield tf.name

    os.unlink(tf.name)


@pytest.mark.repeat(10)
def test_load_from_file_reads_and_processes(temp_file: str):
    result = pytemple.load(temp_file)

    m = re.search(r"value=(\d+)", result)
    assert m is not None

    val = int(m.group(1))
    assert 10 <= val <= 20


@pytest.fixture
def all_placeholders_file() -> Generator[str, None, None]:
    tf = tempfile.NamedTemporaryFile(mode="w", delete=False)
    content = (
        "value_int=${random.int(10,20)}\n"
        "value_double=${random.double(0.5,2.5)}\n"
        "value_bool=${random.boolean}\n"
        "value_string=\"${random.string(8)}\"\n"
        "value_choice=${random.choice(apple,'pear',\"orange\")}\n"
        "value_date=${random.date(2020-01-01, 2020-01-05)}\n"
        "value_datetime=${random.datetime(2020-01-01T00:00:00, 2020-01-02T00:00:00)}\n"
        "value_timestamp=${random.timestamp}\n"
        "value_uuid=${random.uuid}\n"
        "value_past=${random.date.past(days=2)}\n"
        "value_future=${random.date.future(days=3)}\n"
    )
    tf.write(content)
    tf.close()

    yield tf.name

    os.unlink(tf.name)


@pytest.mark.repeat(10)
def test_load_file_with_all_placeholders(all_placeholders_file: str):
    result = pytemple.load(all_placeholders_file)

    # int
    m = re.search(r"value_int=(\d+)", result)
    assert m
    v_int = int(m.group(1))
    assert 10 <= v_int <= 20

    # double
    m = re.search(r"value_double=([+-]?\d+(?:\.\d+)?)", result)
    assert m
    v_double = float(m.group(1))
    assert 0.5 <= v_double <= 2.5

    # boolean
    m = re.search(r"value_bool=(true|false)", result)
    assert m

    # string
    m = re.search(r'value_string="([a-z]{8})"', result)
    assert m
    assert len(m.group(1)) == 8

    # choice
    m = re.search(r"value_choice=([^\s\n]+)", result)
    assert m
    assert m.group(1) in ("apple", "pear", "orange")

    # date
    m = re.search(r"value_date=(\d{4}-\d{2}-\d{2})", result)
    assert m
    d = date.fromisoformat(m.group(1))
    assert date(2020, 1, 1) <= d <= date(2020, 1, 5)

    # datetime
    m = re.search(r"value_datetime=([0-9T:\-]+)", result)
    assert m
    dt = datetime.fromisoformat(m.group(1))
    assert datetime(2020, 1, 1) <= dt <= datetime(2020, 1, 2)

    # timestamp
    m = re.search(r"value_timestamp=(\d+)", result)
    assert m
    ts = int(m.group(1))
    assert abs(int(time.time()) - ts) < 5

    # uuid
    uuid_re = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
    m = uuid_re.search(result)
    assert m

    # past (within 2 days)
    m = re.search(r"value_past=(\d{4}-\d{2}-\d{2})", result)
    assert m
    d_past = date.fromisoformat(m.group(1))
    today = date.today()
    assert today - timedelta(days=2) <= d_past <= today

    # future (within 3 days)
    m = re.search(r"value_future=(\d{4}-\d{2}-\d{2})", result)
    assert m
    d_future = date.fromisoformat(m.group(1))
    assert today <= d_future <= today + timedelta(days=3)
