#version 1.0
#MAE

import PySimpleGUI as sg

def calculator(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

layout = [
    [sg.Text("Введите математическое выражение:")],
    [sg.Input(key="-EXPRESSION-")],
    [sg.Button("Расчет"), sg.Button("Выход")],
    [sg.Text(size=(40, 1), key="-OUTPUT-")],
    [sg.Text("История расчетов:")],
    [sg.Listbox(values=[], size=(45, 6), key="-HISTORY-", select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
]

window = sg.Window("Калькулятор", layout)
history = []

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Выход":
        break

    if event == "Расчет":
        expression = values["-EXPRESSION-"]
        result = calculator(expression)
        window["-OUTPUT-"].update(f"Результат: {result}")

        # Добавляем выражение и результат в историю
        history.append(f"{expression} = {result}")
        # Обновляем список истории на экране
        window["-HISTORY-"].update(values=history)

window.close()

# pyinstaller -w --onefile calcg.py