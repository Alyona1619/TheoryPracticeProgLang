import pytest

from interpreter.interpreter import Interpreter, NodeVisitor
from interpreter.token import Token, TokenType
from interpreter.ast import Number, BinOp, UnaryOp
from interpreter.lexer import Lexer
from interpreter.parser import Parser


@pytest.fixture(scope="function")
def interpreter():
    return Interpreter()


class TestInterpreter:
    interpreter = Interpreter()

    def test_add(self, interpreter):
        assert interpreter.eval("2+2") == 4

    def test_sub(self, interpreter):
        assert interpreter.eval("2-2") == 0

    def test_mult(self, interpreter):
        assert interpreter.eval("2*2") == 4

    def test_del(self, interpreter):
        assert interpreter.eval("2/2") == 1

    def test_add_with_letter(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2+a")

    def test_add_with_letter1(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("t+2")

    def test_wrong_operator(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2&3")

    def test_visit_binop_invalid_operator(self, interpreter):
        left_token = Token(TokenType.NUMBER, '6')
        right_token = Token(TokenType.NUMBER, '2')
        op_token = Token(TokenType.OPERATOR, '&')
        left_node = Number(left_token)
        right_node = Number(right_token)
        binop_node = BinOp(left_node, op_token, right_node)

        with pytest.raises(ValueError, match="Invalid operator"):
            interpreter.visit_binop(binop_node)

    @pytest.mark.parametrize(
        "interpreter, code", [(interpreter, "2 + 2"),
                              (interpreter, "2 +2 "),
                              (interpreter, " 2+2"),
                              (interpreter, "2+2 ")]
    )
    def test_add_spaces(self, interpreter, code):
        assert interpreter.eval(code) == 4

    def test_unary_add(self, interpreter):
        assert interpreter.eval("+2") == 2

    def test_unary_sub(self, interpreter):
        assert interpreter.eval("-2") == -2

    def test_visit_unary_add(self, interpreter):
        number_token = Token(TokenType.NUMBER, '5')
        add_token = Token(TokenType.OPERATOR, '+')
        number_node = Number(number_token)
        unary_op_node = UnaryOp(add_token, number_node)

        result = interpreter.visit_unary(unary_op_node)

        assert result == 5.0

    def test_visit_unary_sub(self, interpreter):
        number_token = Token(TokenType.NUMBER, '3')
        sub_token = Token(TokenType.OPERATOR, '-')
        number_node = Number(number_token)
        unary_op_node = UnaryOp(sub_token, number_node)

        result = interpreter.visit_unary(unary_op_node)

        assert result == -3.0

    def test_visit_unary_invalid_operator(self, interpreter):
        right_token = Token(TokenType.NUMBER, '2')
        op_token = Token(TokenType.OPERATOR, '&')
        right_node = Number(right_token)
        unary_node = UnaryOp(op_token, right_node)

        with pytest.raises(ValueError, match="Invalid operator"):
            interpreter.visit_unary(unary_node)

    def test_number_str(self):
        token = Token(TokenType.NUMBER, "42")
        number_node = Number(token)
        assert str(number_node) == "Number (Token(TokenType.NUMBER, 42))"

    def test_binop_str(self):
        token_plus = Token(TokenType.OPERATOR, "+")
        token_minus = Token(TokenType.OPERATOR, "-")
        left = Number(Token(TokenType.NUMBER, "2"))
        right = Number(Token(TokenType.NUMBER, "3"))
        binop_plus = BinOp(left, token_plus, right)
        binop_minus = BinOp(left, token_minus, right)
        assert str(binop_plus) == "BinOp+ (Number (Token(TokenType.NUMBER, 2)), Number (Token(TokenType.NUMBER, 3)))"
        assert str(
            binop_minus) == "BinOp- (Number (Token(TokenType.NUMBER, 2)), Number (Token(TokenType.NUMBER, 3)))"

    def test_str_with_plus_operator(self):
        plus_token = Token(TokenType.OPERATOR, '+')
        number_token = Token(TokenType.NUMBER, '5')
        number_node = Number(number_token)
        unary_op_node = UnaryOp(plus_token, number_node)

        result = str(unary_op_node)

        assert result == "UnaryOp+ (Number (Token(TokenType.NUMBER, 5)))"


@pytest.fixture(scope="function")
def lexer():
    return Lexer()


class TestLexer:
    lexer = Lexer()

    def test_opening_parenthesis(self, lexer):
        lexer.init("(")
        token = lexer.next()
        assert token.type_ == TokenType.LPAREN
        assert token.value == "("

    def test_closing_parenthesis(self, lexer):
        lexer.init(")")
        token = lexer.next()
        assert token.type_ == TokenType.RPAREN
        assert token.value == ")"


@pytest.fixture(scope="function")
def parser():
    return Parser()


class TestParser:
    parser = Parser()

    def test_check_token_valid(self, parser):
        token = Token(TokenType.NUMBER, "42")
        parser._current_token = token
        parser.check_token(TokenType.NUMBER)

    def test_check_token_invalid(self, parser):
        token = Token(TokenType.OPERATOR, "+")
        parser._current_token = token
        with pytest.raises(SyntaxError):
            parser.check_token(TokenType.NUMBER)

    def test_factor_with_opening_parenthesis(self, parser):
        code = "(2 + 3 * 4)"
        result = parser.parse(code)
        assert str(
            result) == "BinOp+ (Number (Token(TokenType.NUMBER, 2)), BinOp* (Number (Token(TokenType.NUMBER, 3)), Number (Token(TokenType.NUMBER, 4))))"

    def test_invalid_operator_factor(self, parser):
        code = "2 * + 3 * 4"
        with pytest.raises(SyntaxError, match="Invalid factor"):
            parser.parse(code)

    def test_missing_closing_parentheses_factor(self, parser):
        code = "2 * (3 + 4"
        with pytest.raises(SyntaxError, match="Invalid factor"):
            parser.parse(code)
