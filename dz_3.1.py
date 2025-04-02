from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout
)


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация пользователя")
        self.setFixedSize(400, 250)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.login_label = QLabel("Введите логин:")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.password_label = QLabel("Введите пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")

        self.register_button = QPushButton("Зарегистрировать")

        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = RegistrationWindow()
    window.show()
    app.exec()