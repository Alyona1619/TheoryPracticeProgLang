from .token import Token


class Node:
    pass


class Number(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):  # pragma: no cover
        return f"Number ({self.token})"


class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):  # pragma: no cover
        return f"BinOp{self.op.value} ({self.left}, {self.right})"


class UnaryOp(Node):
    def __init__(self, op: Token, right: Node):
        self.op = op
        self.right = right

    def __str__(self):  # pragma: no cover
        return f"UnaryOp{self.op.value} ({self.right})"


class Empty(Node):
    def __init__(self, value=""):
        self.value = value


class Variable(Node):
    def __init__(self, token, value):
        self.token = token
        self.value = value


class Identifier(Node):
    def __init__(self, token):
        self.token = token


class Semicolon(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right