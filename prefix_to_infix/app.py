from src.prefix_to_infix import to_infix


def main():
    print("Конвертер префиксной нотации в инфиксную")
    input_expression = input("Введите выражение в префиксной нотации: ")
    infix_expression = to_infix(input_expression)
    print("Инфиксная запись выражения:", infix_expression)


if __name__ == "__main__":
    main()
