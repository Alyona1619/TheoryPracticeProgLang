from .parser import Parser
from .ast import Number, BinOp, UnaryOp, Variable, Semicolon, Empty, Identifier


class NodeVisitor:
    pass


class Interpreter(NodeVisitor):

    def __init__(self):
        self.parser = Parser()
        self.variables = {}

    def visit(self, node):
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, Variable):
            return self.visit_variable(node)
        elif isinstance(node, Semicolon):
            return self.visit_semicolon(node)
        elif isinstance(node, Empty):
            pass
        elif isinstance(node, Identifier):
            return self.visit_identifier(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary(node)
        return 0.0

    def visit_number(self, node):
        return float(node.token.value)

    def visit_binop(self, node):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)
            case "-":
                return self.visit(node.left) - self.visit(node.right)
            case "*":
                return self.visit(node.left) * self.visit(node.right)
            case "/":
                return self.visit(node.left) / self.visit(node.right)
            case _:
                raise ValueError(f"Invalid operator: {node.op.value}")

    def visit_unary(self, node):
        match node.op.value:
            case "+":
                return self.visit(node.right)
            case "-":
                return -self.visit(node.right)
            case _:
                raise ValueError("Invalid operator")

    def visit_identifier(self, node):
        if node.token.value in self.variables:
            return self.variables[node.token.value]
        raise ValueError("Unknown variable")

    def visit_semicolon(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_variable(self, node):
        if node.token.value not in self.variables:
            self.variables[node.token.value] = 0.0
        self.variables[node.token.value] = self.visit(node.value)

    def eval(self, code):
        tree = self.parser.parse(code)
        #if tree is None:  # Handle empty AST
        #    return 0
        return self.visit(tree)

# interpreter = Interpreter()
# result = interpreter.eval("x = 5 + 3; y = x * 2; y + 1")
# print(result)