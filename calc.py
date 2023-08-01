def calculator(expression):
    try:
        result = eval(expression)
        return result
    except Exception as error:
        return error
while True:
    expression = input("Введите выражение: ")
    if expression.strip() == '':
        break
    result = calculator(expression)
    print("Результат: ", result)
    print("Для выхода нажать Enter")
