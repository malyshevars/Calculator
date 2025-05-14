import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QMenuBar, QAction, QSystemTrayIcon, QStyle,
    QMessageBox
)
from PyQt5.QtCore import Qt

def calculator(expr):
    try:
        return eval(expr)
    except Exception as e:
        return f"Ошибка: {e}"

app = QApplication(sys.argv)

dark_style = """
QWidget {
    background-color: #2b2b2b;
    color: #eeeeee;
    font-family: Arial;
    font-size: 14px;
}
QLineEdit {
    background-color: #3c3f41;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
}
QPushButton {
    background-color: #4b6eaf;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #6a8ec0;
}
QListWidget {
    background-color: #353839;
    border: 1px solid #555555;
    border-radius: 4px;
}
"""

flat_light = """
QWidget {
    background-color: #f7f7f7;
    color: #333333;
    font-family: "Segoe UI";
    font-size: 13px;
}
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 2px;
    padding: 5px;
}
QPushButton {
    background-color: #e1e1e1;
    border: 1px solid #bbbbbb;
    border-radius: 2px;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: #d4d4d4;
}
QListWidget {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 2px;
}
"""

vibrant = """
QWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ffd89b, stop:1 #19547b);
    color: #222222;
    font-family: Verdana;
    font-size: 14px;
}
QLineEdit {
    background: rgba(255,255,255,0.8);
    border: 1px solid #ffffff;
    border-radius: 6px;
    padding: 6px;
}
QPushButton {
    background-color: #ffd89b;
    border: 2px solid #19547b;
    border-radius: 6px;
    padding: 6px 14px;
}
QPushButton:hover {
    background-color: #ffe5b4;
}
QListWidget {
    background: rgba(255,255,255,0.8);
    border: 1px solid #ffffff;
    border-radius: 6px;
}
"""

gradient_style = """
QWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #89f7fe, stop:1 #66a6ff);
    font-family: Arial;
}
QLabel {
    color: #333;
    font-size: 14px;
}
SmartLineEdit, QLineEdit {
    background: #fff;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 4px;
}
QPushButton {
    background: #ffffff;
    border: 1px solid #bbb;
    border-radius: 4px;
    padding: 6px 12px;
}
QPushButton:hover {
    background: #f0f0f0;
}
QListWidget {
    background: #fafafa;
    border: 1px solid #ccc;
    border-radius: 4px;
}
"""

app.setStyleSheet(vibrant)  # стиль по умолчанию


win = QWidget()
win.setWindowTitle("Калькулятор AE")
win.resize(400, 300)


menubar = QMenuBar(win)


main_menu = menubar.addMenu("Главное")
action_help     = QAction("Справка", win)
action_about    = QAction("О программе", win)
action_minimize = QAction("Свернуть в трей", win)
main_menu.addAction(action_help)
main_menu.addAction(action_about)
main_menu.addSeparator()
main_menu.addAction(action_minimize)


style_menu = menubar.addMenu("Вид")
action_dark     = QAction("Тёмная тема", win)
action_light    = QAction("Светлая тема", win)
action_vibrant  = QAction("Яркая тема", win)
action_gradient = QAction("Градиентный", win)
action_dark.triggered.connect(lambda: app.setStyleSheet(dark_style))
action_light.triggered.connect(lambda: app.setStyleSheet(flat_light))
action_vibrant.triggered.connect(lambda: app.setStyleSheet(vibrant))
action_gradient.triggered.connect(lambda: app.setStyleSheet(gradient_style))
for a in (action_dark, action_light, action_vibrant, action_gradient):
    style_menu.addAction(a)

layout = QVBoxLayout(win)
layout.setMenuBar(menubar)


lbl         = QLabel("Введите выражение:")
input_expr  = QLineEdit()
input_expr.setPlaceholderText("Сюда")
input_expr.returnPressed.connect(lambda: btn_calc.click())

btn_clear   = QPushButton("Очистить историю")
btn_calc    = QPushButton("Вычислить")
lbl_result  = QLabel("")
lbl_result.setAlignment(Qt.AlignCenter)
lbl_hist    = QLabel("История расчетов:")
list_history= QListWidget()
list_history.addItem("Нет результатов...")
history     = []


btn_layout = QHBoxLayout()
btn_layout.addWidget(btn_clear)
btn_layout.addWidget(btn_calc)


layout.addWidget(lbl)
layout.addWidget(input_expr)
layout.addLayout(btn_layout)
layout.addWidget(lbl_result)
layout.addWidget(lbl_hist)
layout.addWidget(list_history)


def do_calc():
    expr = input_expr.text().strip()
    if not expr:
        return
    if not history:
        list_history.clear()
    res = calculator(expr)
    record = f"{expr} = {res}"
    history.append(record)
    list_history.addItem(record)
    lbl_result.setText(f"Результат: {res}")
    input_expr.clear()

def clear_hist():
    history.clear()
    lbl_result.clear()
    list_history.clear()
    list_history.addItem("Нет результатов...")

def load_hist(item):
    text = item.text()
    if text == "Нет результатов...":
        return
    expr, _ = text.split(" = ", 1)
    input_expr.setText(expr)
    input_expr.setFocus()

btn_calc.clicked.connect(do_calc)
btn_clear.clicked.connect(clear_hist)
list_history.itemClicked.connect(load_hist)


trayIcon = QSystemTrayIcon(
    app.style().standardIcon(QStyle.SP_ComputerIcon),
    parent=win
)
trayIcon.setToolTip("Калькулятор AE")

def on_tray_activated(reason):
    if reason == QSystemTrayIcon.Trigger:
        win.showNormal()
        win.activateWindow()

trayIcon.activated.connect(on_tray_activated)
trayIcon.show()


def show_help():
    info = (
        "• Enter: выполнить вычисление.\n"
        "• Esc: свернуть окно в трей.\n"
        "• 'Вид': смена темы оформления.\n"
        "• 'Очистить историю': удалить все записи в истории.\n"
        "• Клик по истории: загрузить выражение обратно в поле.\n"
        "• Клик по результату: скопировать в буфер обмена."
    )
    QMessageBox.information(win, "Справка", info)

action_help.triggered.connect(show_help)


def show_about():
    QMessageBox.about(win, "О программе",
        "Калькулятор AE\nВерсия 2.0\n2025")

action_about.triggered.connect(show_about)

action_minimize.triggered.connect(lambda: win.hide())


def keyPressEvent(event):
    if event.key() == Qt.Key_Escape:
        win.hide()
    else:
        QWidget.keyPressEvent(win, event)

def closeEvent(event):
    trayIcon.hide()
    event.accept()
    QApplication.quit()

win.keyPressEvent = keyPressEvent
win.closeEvent    = closeEvent


lbl_result.setCursor(Qt.PointingHandCursor)
lbl_result.mousePressEvent = lambda e: QApplication.clipboard().setText(
    lbl_result.text().replace("Результат: ", "")
)


win.show()
sys.exit(app.exec_())
