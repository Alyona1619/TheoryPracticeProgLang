from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    EOL = auto()
    LPAREN = auto()
    RPAREN = auto()
    BEGIN = auto()
    END = auto()
    DOT = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
    ID = auto()


class Token:

    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self):  # pragma: no cover
        return f"Token({self.type_}, {self.value})"
