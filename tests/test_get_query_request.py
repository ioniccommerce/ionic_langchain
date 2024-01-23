import pytest

from ionic_langchain.tool import Ionic


def test_none_input_raises_value_error():
    ionic = Ionic()
    with pytest.raises(ValueError):
        ionic.gen_query_request(None)


def test_only_spaces_input_raises_value_error():
    ionic = Ionic()
    with pytest.raises(ValueError):
        ionic.gen_query_request("   ,   ,   ,   ")


def test_extra_values_ignores_extra_values():
    ionic = Ionic()
    result = ionic.gen_query_request("test query, 2, 1, 3, extra, values")
    assert result == ("test query", 2, 1, 3)


def test_negative_number_values_raises_value_error():
    ionic = Ionic()
    result = ionic.gen_query_request("test query, -2, -1, -3")
    assert result == ("test query", None, None, None)


def test_valid_input_returns_expected_output():
    ionic = Ionic()
    result = ionic.gen_query_request("test query, 2, 1, 3")

    assert result == ("test query", 2, 1, 3)


def test_missing_values_returns_expected_output():
    ionic = Ionic()
    result = ionic.gen_query_request("test query, , , ")

    assert result == ("test query", None, None, None)


def test_extra_spaces_returns_expected_output():
    ionic = Ionic()
    result = ionic.gen_query_request("  test query  ,  2  ,  1  ,  3  ")

    assert result == ("test query", 2, 1, 3)


def test_invalid_number_values_raises_value_error():
    ionic = Ionic()
    with pytest.raises(ValueError):
        ionic.gen_query_request("test query, not a number, not a number, not a number")


def test_float_raises_value_error():
    ionic = Ionic()
    with pytest.raises(ValueError):
        ionic.gen_query_request("test, 1.0, 2.0, 3.0")
