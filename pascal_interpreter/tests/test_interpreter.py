import pytest

from interpreter.interpreter import Interpreter, NodeVisitor
from interpreter.token import Token, TokenType
from interpreter.ast import Number, BinOp, UnaryOp


@pytest.fixture
def interpreter():
    return Interpreter()


def test_code_1(interpreter):
    code = """
       BEGIN
       END.
    """
    result = interpreter.eval(code)
    assert result == 0
    assert interpreter.variables == {}


def test_code_2(interpreter):
    code = """
        BEGIN
            x := 2 + 3 * (2 + 3);
            y := 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));
        END.
    """
    interpreter.eval(code)
    res = interpreter.variables
    assert res == {'x': 17.0, 'y': 11.0}


def test_code_3(interpreter):
    code = """
        BEGIN
            y := 2;
            BEGIN
                a := 3;
                a := a;
                b := 10 + a + 10 * y / 4;
                c := a - b
            END;
            x := 11;
        END.
    """
    interpreter.eval(code)
    res = interpreter.variables
    assert res == {'y': 2.0, 'a': 3.0, 'b': 18.0, 'c': -15.0, 'x': 11.0}


def test_valid_unaryop(interpreter):
    code = """
        BEGIN
            y := -3;
            x := +24;
        END.
    """
    interpreter.eval(code)
    res = interpreter.variables
    assert res == {'y': -3.0, 'x': 24.0}


def test_invalid_begin(interpreter):
    code = """
            x := 2;
            y := 2;
        END.
    """.strip()
    with pytest.raises(ValueError):
        interpreter.eval(code)


def test_invalid_end(interpreter):
    code = """
        BEGIN
            x := 2;
            y := 2;
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)


def test_invalid_binop(interpreter):
    code = """
        BEGIN
            y := 2 @ 4;
        END.
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)



def test_invalid_unaryop(interpreter):
    code = """
        BEGIN
            y := /4;
        END.
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)

def test_invalid_expression(interpreter):
    code = """
        BEGIN
            x := 2 + ~3;
        END.
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)



def test_invalid_var(interpreter):
    code = """
        BEGIN
            x := +++;
        END.
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)


def test_invalid_lexer(interpreter):
    code = """
        BEGIN
            x + 1;
        END.
    """
    with pytest.raises(SyntaxError):
        interpreter.eval(code)


def test_invalid_assign(interpreter):
    code = """
        BEGIN
            x :* 3;
        END.
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)


def test_invalid_assign1(interpreter):
    code = """
        BEGIN
            := 2;
        END.
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)


def test_unknown_var(interpreter):
    code = """
        BEGIN
            x := 2;
            y := x + 1 + z;
        END.
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)


def test_invalid_namevar(interpreter):
    code = """
        BEGIN
            Big := 2;
        END.
    """
    with pytest.raises(ValueError):
        interpreter.eval(code)

def test_invalid_parentheses_matching(interpreter):
    code = """
        BEGIN
            x := (2 + 3 * 4;
        END.
    """
    with pytest.raises(SyntaxError):
        interpreter.eval(code)


def test_division_by_zero(interpreter):
    code = """
        BEGIN
            x := 1 / 0;
        END.
    """
    with pytest.raises(ZeroDivisionError):
        interpreter.eval(code)


def test_visit_binop_invalid_operator(interpreter):
    left_token = Token(TokenType.NUMBER, '6')
    right_token = Token(TokenType.NUMBER, '2')
    op_token = Token(TokenType.OPERATOR, '&')
    left_node = Number(left_token)
    right_node = Number(right_token)
    binop_node = BinOp(left_node, op_token, right_node)

    with pytest.raises(ValueError, match="Invalid operator"):
        interpreter.visit_binop(binop_node)




