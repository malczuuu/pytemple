import pytemple


def test_should_parse_int_pattern():
    result = pytemple.loads('${random.int(0, 30)}')

    res_int = int(result)

    assert 0 <= res_int <= 30
