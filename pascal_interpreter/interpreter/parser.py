from .token import Token, TokenType
from .lexer import Lexer
from .ast import BinOp, Number, UnaryOp, Identifier, Variable, Semicolon, Empty


class Parser:
    def __init__(self):
        self._current_token = None
        self._lexer = Lexer()

    def check_token(self, type_: TokenType):
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next()
        else:
            raise SyntaxError("invalid token order")

    def factor(self):
        token = self._current_token
        #if token is None:
        #    return Empty()
        if token.type_ == TokenType.NUMBER:
            self.check_token(TokenType.NUMBER)
            return Number(token)
        elif token.type_ == TokenType.LPAREN:
            self.check_token(TokenType.LPAREN)
            result = self.expr()
            self.check_token(TokenType.RPAREN)
            return result
        elif token.type_ == TokenType.OPERATOR:
            self.check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.factor())
        elif token.type_ == TokenType.ID:
            self.check_token(TokenType.ID)
            return Identifier(token)
        elif token.type_ == TokenType.BEGIN:
            return self.complex_statement()
        else:
            print(f"Invalid factor: {token.type_}, {token.value}")
            raise ValueError("Invalid factor")

    # def term(self):
    #     result = self.factor()
    #     while self._current_token and self._current_token.type_ == TokenType.OPERATOR and self._current_token.value in "*/":
    #         token = self._current_token
    #         self.check_token(TokenType.OPERATOR)
    #         result = BinOp(result, token, self.term())
    #     return result

    def term(self):
        result = self.factor()
        while self._current_token and self._current_token.type_ == TokenType.OPERATOR and self._current_token.value in "*/":
            token = self._current_token
            self.check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.term())
        return result

    def expr(self):
        #if self._current_token is None:
        #    return Empty()
        result = self.term()
        while self._current_token is not None and self._current_token.type_ == TokenType.OPERATOR:
            token = self._current_token
            self.check_token(TokenType.OPERATOR)
            #if self._current_token is None:
            #    return Empty()
            result = BinOp(result, token, self.term())
        return result

    def variable(self):
        result = self._current_token
        self.check_token(TokenType.ID)
        return result

    def assignment(self):
        id_token = self.variable()
        self.check_token(TokenType.ASSIGN)
        return Variable(id_token, self.expr())

    def complex_statement(self):
        self.check_token(TokenType.BEGIN)
        result = self.statement_list()
        self.check_token(TokenType.END)
        return result

    def statement_list(self):
        result = self.statement()
        if self._current_token.type_ == TokenType.SEMICOLON:
            self.check_token(TokenType.SEMICOLON)
            result = Semicolon(result, self.statement_list())
        return result

    def statement(self):
        if self._current_token is None:
            raise ValueError("Unexpected end of input")

        token_type = self._current_token.type_

        if token_type == TokenType.BEGIN:
            return self.complex_statement()
        elif token_type == TokenType.ID:
            return self.assignment()
        elif token_type == TokenType.END:
            return self.empty()
        else:
            raise ValueError("Invalid token")

    def empty(self):
        return Empty()

    # def parse_main(self):
    #     result = self.complex_statement()
    #     self.check_token(TokenType.DOT)
    #     return result

    def parse(self, code):
        self._lexer.init(code)
        self._current_token = self._lexer.next()
        return self.expr()
