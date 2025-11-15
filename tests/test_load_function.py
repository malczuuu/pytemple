import os
import re
import tempfile
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
