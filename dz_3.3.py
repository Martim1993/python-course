from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QPushButton, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout)


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простой блокнот")
        self.setGeometry(100, 100, 600, 500)
        self.text_edit = QTextEdit()
        self.save_button = QPushButton("Сохранить")
        self.open_button = QPushButton("Открыть")
        self.save_button.clicked.connect(self.save_file)
        self.open_button.clicked.connect(self.open_file)
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.open_button)
        layout.addLayout(buttons_layout)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text_edit.setText(file.read())


if __name__ == "__main__":
    app = QApplication([])
    notepad = Notepad()
    notepad.show()
    app.exec()