import pytest
from ..src.prefix_to_infix import to_infix, is_operator


@pytest.fixture
def operators():
    return '+', '-', '*', '/'


def test_valid_prefix_expression():
    expression = "+ - 13 4 55"
    result = to_infix(expression)
    assert result == "((13 - 4) + 55)"


def test_invalid_prefix_expression():
    expression = "+ - 13 4 55 10"
    with pytest.raises(ValueError) as e_info:
        to_infix(expression)


def test_empty_prefix_expression():
    expression = ""
    with pytest.raises(ValueError) as e_info:
        to_infix(expression)


def test_operator_precedence():
    expression = "+ * 2 3 - 5 4"
    result = to_infix(expression)
    assert result == "((2 * 3) + (5 - 4))"


def test_is_operator():
    oper = '/'
    result = is_operator(oper)
    assert result == True


def test_is_operator1():
    oper = '+'
    result = is_operator(oper)
    assert result == True
