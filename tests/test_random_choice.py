import pytest

import pytemple


@pytest.mark.repeat(10)
def test_choice_membership_unquoted():
    result = pytemple.loads("${random.choice(apple,banana,pear)}")

    assert result in ("apple", "banana", "pear")


@pytest.mark.repeat(10)
def test_choice_with_quotes_and_spaces():
    src = '${random.choice("hello world","foo bar",baz)}'
    result = pytemple.loads(src)

    assert result in ("hello world", "foo bar", "baz")


def test_choice_single_arg_returns_it():
    src = "${random.choice(single)}"

    assert pytemple.loads(src) == "single"


def test_choice_malformed_unmatched_quote_not_replaced():
    src = "${random.choice('unmatched,good)}"

    assert pytemple.loads(src) == src
