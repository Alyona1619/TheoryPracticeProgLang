def is_operator(operator):
    return operator in ['+', '-', '*', '/']


def to_infix(expression):
    stack = []
    operators = expression.split()
    for operator in reversed(operators):
        if operator.isdigit():
            stack.append(operator)
        elif is_operator(operator):
            operand1 = stack.pop()
            operand2 = stack.pop()
            infix_expression = f"({operand1} {operator} {operand2})"
            stack.append(infix_expression)
        else:
            raise ValueError(f"Неизестный оператор: {operator}")

    if len(stack) != 1:
        raise ValueError("Некорректное выражение")

    return stack[0]


def main():
    try:
        print("Конвертер префиксной нотации в инфиксную")
        input_expression = input("Введите выражение в префиксной нотации: ")
        infix_expression = to_infix(input_expression)
        print("Инфиксная запись выражения:", infix_expression)
    except ValueError as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
