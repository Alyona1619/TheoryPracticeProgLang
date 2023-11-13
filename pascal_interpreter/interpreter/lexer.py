from .token import Token, TokenType


class Lexer():

    def __init__(self):
        self._pos = 0
        self._text = ""
        self._current_char = None

    def init(self, text):
        self._text = text
        self._pos = 0
        self._current_char = self._text[self._pos]

    def forward(self):
        self._pos += 1
        if self._pos > len(self._text) - 1:
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def skip(self):
        while (self._current_char is not None and
               self._current_char.isspace()):
            self.forward()

    def number(self):
        result = []
        while (self._current_char is not None and
               (self._current_char.isdigit() or
                self._current_char == ".")):
            result.append(self._current_char)
            self.forward()
        return "".join(result)

    def variable(self):
        result = []
        while self._current_char is not None and (self._current_char.isalpha() or self._current_char.isdigit()):
            result.append(self._current_char)
            self.forward()
        return ''.join(result)

    def next(self):
        while self._current_char is not None:
            current_char = self._current_char
            if current_char.isspace():
                self.skip()
                continue
            if current_char == 'B':
                begin = ['E', 'G', 'I', 'N']
                result = []
                self.forward()
                for i in begin:
                    current_char = self._current_char
                    result.append(current_char)
                    self.forward()
                if result == begin:
                    return Token(TokenType.BEGIN, "BEGIN")
                raise ValueError("Invalid variable")
            if current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())
            if current_char in ['+', '-', '*', '/']:
                op = current_char
                self.forward()
                return Token(TokenType.OPERATOR, op)
            if current_char in ['(', ')']:
                paren = current_char
                self.forward()
                return Token(TokenType.LPAREN, paren) if paren == '(' else Token(TokenType.RPAREN, paren)
            if current_char == ';':
                self.forward()
                return Token(TokenType.SEMICOLON, ";")
            if current_char == '.':
                self.forward()
                return Token(TokenType.DOT, ".")
            if current_char == ':':
                self.forward()
                #while self._current_char is not None and self._current_char.isspace():
                #    self.forward()
                if self._current_char == '=':
                    self.forward()
                    return Token(TokenType.ASSIGN, "=")
                raise ValueError("Invalid syntax")
            if current_char == 'E':
                end = ['N', 'D']
                result = []
                self.forward()
                for i in end:
                    current_char = self._current_char
                    result.append(current_char)
                    self.forward()
                if result == end:
                    return Token(TokenType.END, "END")
                #raise ValueError("Invalid variable")
            if current_char.isalpha():
                return Token(TokenType.ID, self.variable())
            raise ValueError("Invalid token")
        return None


