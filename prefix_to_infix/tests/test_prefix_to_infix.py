import pytest
from ..src.prefix_to_infix import to_infix, is_operator


@pytest.fixture
def operators():
    return '+', '-', '*', '/'


@pytest.fixture
def valid_expressions():
    return (
        ('+ - 13 4 55', '((13 - 4) + 55)'),
        ('+ 2 * 2 - 2 1', '(2 + (2 * (2 - 1)))'),
        ('/ + 3 10 * + 2 3 - 3 5', '((3 + 10) / ((2 + 3) * (3 - 5)))'),
        ('+ + 10 20 30', '((10 + 20) + 30)'),
    )


class TestPrToIn:

    def test_valid_expression(self, valid_expressions):
        for prefix_expression, expected_infix_expression in valid_expressions:
            result = to_infix(prefix_expression)
            assert result == expected_infix_expression

    def test_invalid_expression(self):
        expression = "+ - 13 4 55 10"
        with pytest.raises(ValueError) as e_info:
            to_infix(expression)

    def test_invalid_operand(self):
        invalid_inputs = ["+ a 2", "/ 3 b", "* x y"]

        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError, match="Неизвестный оператор или операнд"):
                to_infix(invalid_input)

    def test_empty_expression(self):
        expression = ""
        with pytest.raises(ValueError) as e_info:
            to_infix(expression)

    def test_more_operands(self):
        with pytest.raises(ValueError, match="Операторов больше, чем нужно для операндов"):
            to_infix("- - 1 2")

    def test_is_operator(self, operators):
        op1, op2, op3, op4 = operators
        res = is_operator(op1)
        res1 = is_operator(op2)
        res2 = is_operator(op3)
        res3 = is_operator(op4)
        assert res == res1 == res2 == res3 is True

    def test_invalid_operator(self):
        with pytest.raises(ValueError, match=f"Неизвестный оператор или операнд: @"):
            to_infix("@ 1 2")
