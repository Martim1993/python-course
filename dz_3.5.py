import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
import sqlite3


class EmployeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет сотрудников")
        self.setGeometry(100, 100, 400, 300)

        self.conn = sqlite3.connect('employees.db')
        self.create_table()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.form_layout = QFormLayout()

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.position_input = QLineEdit()

        self.form_layout.addRow("Имя:", self.first_name_input)
        self.form_layout.addRow("Фамилия:", self.last_name_input)
        self.form_layout.addRow("Возраст:", self.age_input)
        self.form_layout.addRow("Должность:", self.position_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_employee)

        self.status_label = QLabel("Введите данные сотрудника")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.save_button)
        self.main_layout.addWidget(self.status_label)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER,
                position TEXT
            )
        ''')
        self.conn.commit()

    def save_employee(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        age = self.age_input.text().strip()
        position = self.position_input.text().strip()

        if not first_name or not last_name:
            QMessageBox.warning(self, "Ошибка", "Имя и фамилия обязательны для заполнения!")
            return

        try:
            age = int(age) if age else None
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Возраст должен быть числом!")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO employees (first_name, last_name, age, position)
                VALUES (?, ?, ?, ?)
            ''', (first_name, last_name, age, position))
            self.conn.commit()

            self.first_name_input.clear()
            self.last_name_input.clear()
            self.age_input.clear()
            self.position_input.clear()

            self.status_label.setText("Данные успешно сохранены!")
            QMessageBox.information(self, "Успех", "Данные сотрудника сохранены в базу данных!")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Произошла ошибка: {str(e)}")

    def closeEvent(self, event):
        """Закрывает соединение с базой данных при закрытии приложения"""
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmployeeApp()
    window.show()
    sys.exit(app.exec())