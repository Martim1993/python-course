import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QFileDialog,
                             QToolBar, QStatusBar, QMessageBox)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовый редактор")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()

        self.current_file = None

    def create_menu(self):
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("&Файл")

        new_action = QAction(QIcon.fromTheme("document-new"), "&Создать", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon.fromTheme("document-open"), "&Открыть", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon.fromTheme("document-save"), "&Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction(QIcon.fromTheme("application-exit"), "&Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Правка
        edit_menu = menubar.addMenu("&Правка")

        cut_action = QAction(QIcon.fromTheme("edit-cut"), "Вырезать", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon.fromTheme("edit-copy"), "Копировать", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon.fromTheme("edit-paste"), "Вставить", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

    def create_toolbar(self):
        toolbar = QToolBar("Панель инструментов")
        self.addToolBar(toolbar)

        # Добавляем те же действия, что и в меню
        actions = [
            ("document-new", "Создать", self.new_file, "Ctrl+N"),
            ("document-open", "Открыть", self.open_file, "Ctrl+O"),
            ("document-save", "Сохранить", self.save_file, "Ctrl+S"),
            None,  # Разделитель
            ("edit-cut", "Вырезать", self.text_edit.cut, "Ctrl+X"),
            ("edit-copy", "Копировать", self.text_edit.copy, "Ctrl+C"),
            ("edit-paste", "Вставить", self.text_edit.paste, "Ctrl+V"),
        ]

        for action in actions:
            if action is None:
                toolbar.addSeparator()
            else:
                icon, text, slot, shortcut = action
                act = QAction(QIcon.fromTheme(icon), text, self)
                act.triggered.connect(slot)
                act.setShortcut(shortcut)
                toolbar.addAction(act)

    def create_statusbar(self):
        self.statusBar().showMessage("Готово")

    def new_file(self):
        self.text_edit.clear()
        self.current_file = None
        self.statusBar().showMessage("Создан новый файл")

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.text_edit.setText(f.read())
                self.current_file = filename
                self.statusBar().showMessage(f"Открыт файл: {filename}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")

    def save_file(self):
        if self.current_file:
            filename = self.current_file
        else:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Сохранить файл", "", "Текстовые файлы (*.txt);;Все файлы (*)"
            )
            if not filename:
                return  # Пользователь отменил диалог

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())
            self.current_file = filename
            self.statusBar().showMessage(f"Файл сохранён: {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def closeEvent(self, event):
        if not self.text_edit.toPlainText():
            event.accept()
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы хотите сохранить изменения перед выходом?',
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save
        )

        if reply == QMessageBox.StandardButton.Save:
            self.save_file()
            event.accept()
        elif reply == QMessageBox.StandardButton.Discard:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())