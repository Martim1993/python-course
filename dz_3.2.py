from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget)


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setFixedSize(300, 400)
        self.current_expression = ""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', 'C', '=', '+']
        ]

        for row in buttons:
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            row_widget.setLayout(row_layout)

            for btn_text in row:
                button = QPushButton(btn_text)
                button.setFixedSize(60, 60)
                button.clicked.connect(self.on_button_click)
                row_layout.addWidget(button)

            main_layout.addWidget(row_widget)

    def on_button_click(self):
        button = self.sender()
        text = button.text()

        if text == "=":
            try:
                result = eval(self.current_expression)
                print(f"Результат: {self.current_expression} = {result}")
                self.current_expression = str(result)
            except Exception as e:
                print(f"Ошибка: {e}")
                self.current_expression = ""
        elif text == "C":
            self.current_expression = ""
        else:
            self.current_expression += text
            print(f"Текущее выражение: {self.current_expression}")


if __name__ == "__main__":
    app = QApplication([])
    calculator = Calculator()
    calculator.show()
    app.exec()