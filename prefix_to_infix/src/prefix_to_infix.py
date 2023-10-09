def is_operator(operator):
    return operator in ['+', '-', '*', '/']


def to_infix(expression):
    stack = []
    operators = expression.split()
    for operator in reversed(operators):
        if operator.isdigit():
            stack.append(operator)
        elif is_operator(operator):
            if len(stack) < 2:
                raise ValueError("Операторов больше, чем нужно для операндов")
            operand1 = stack.pop()
            operand2 = stack.pop()
            infix_expression = f"({operand1} {operator} {operand2})"
            stack.append(infix_expression)
        else:
            raise ValueError(f"Неизвестный оператор или операнд: {operator}")

    if len(stack) != 1:
        raise ValueError("Некорректное выражение")

    return stack[0]
