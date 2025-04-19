from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QRadioButton, QButtonGroup, QComboBox, QLabel
)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.line_edit = QLineEdit()
        self.button = QPushButton('Нажми меня')
        self.combo_box = QComboBox()
        self.radio_group = QButtonGroup()
        self.combo_box.addItems(["Пункт 1", "Пункт 2", "Пункт 3"])
        radio1 = QRadioButton("Вариант 1")
        radio2 = QRadioButton("Вариант 2")
        radio3 = QRadioButton("Вариант 3")
        self.radio_group.addButton(radio1, 1)
        self.radio_group.addButton(radio2, 2)
        self.radio_group.addButton(radio3, 3)
        radio1.setChecked(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Текстовое поле:"))
        layout.addWidget(self.line_edit)
        layout.addWidget(QLabel("Радио-кнопки:"))
        layout.addWidget(radio1)
        layout.addWidget(radio2)
        layout.addWidget(radio3)
        layout.addWidget(QLabel("Комбобокс:"))
        layout.addWidget(self.combo_box)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.print_to_console)
        self.combo_box.currentTextChanged.connect(self.update_button_text)
        self.line_edit.textChanged.connect(self.toggle_button_state)
        self.toggle_button_state(self.line_edit.text())
        self.setWindowTitle('PyQt6 Приложение')
        self.setGeometry(300, 300, 300, 200)

    def print_to_console(self):
        text = self.line_edit.text()
        combo_text = self.combo_box.currentText()
        radio_text = self.radio_group.checkedButton().text()
        print(f"Текст: {text}")
        print(f"Выбран комбобокс: {combo_text}")
        print(f"Выбрана радио-кнопка: {radio_text}")
        print("-" * 30)

    def update_button_text(self, text):
        self.button.setText(f"Выбрано: {text}")

    def toggle_button_state(self, text):
        self.button.setEnabled(bool(text.strip()))


if __name__ == '__main__':
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()