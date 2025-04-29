import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QFileDialog,
                             QMessageBox, QToolBar, QStatusBar)
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6.QtGui import QIcon, QAction


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_file = None

    def initUI(self):
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.init_menus()

        self.init_toolbar()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Блокнот')
        self.show()

    def init_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&Файл')

        new_action = QAction(QIcon.fromTheme('document-new'), '&Новый', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Создать новый файл')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon.fromTheme('document-open'), '&Открыть', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Открыть файл')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon.fromTheme('document-save'), '&Сохранить', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Сохранить файл')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction(QIcon.fromTheme('document-save-as'), 'Сохранить &как...', self)
        save_as_action.setStatusTip('Сохранить файл как...')
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        print_action = QAction(QIcon.fromTheme('document-print'), '&Печать...', self)
        print_action.setShortcut('Ctrl+P')
        print_action.setStatusTip('Распечатать документ')
        print_action.triggered.connect(self.print_document)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        exit_action = QAction(QIcon.fromTheme('application-exit'), '&Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Выйти из программы')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('&Правка')

        undo_action = QAction(QIcon.fromTheme('edit-undo'), '&Отменить', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.setStatusTip('Отменить последнее действие')
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon.fromTheme('edit-redo'), '&Вернуть', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.setStatusTip('Вернуть отмененное действие')
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon.fromTheme('edit-cut'), 'Выре&зать', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.setStatusTip('Вырезать выделенный текст')
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon.fromTheme('edit-copy'), '&Копировать', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.setStatusTip('Копировать выделенный текст')
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon.fromTheme('edit-paste'), 'Вст&авить', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.setStatusTip('Вставить текст из буфера обмена')
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        select_all_action = QAction('Выделить &все', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.setStatusTip('Выделить весь текст')
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)

        help_menu = menubar.addMenu('&Справка')

        about_action = QAction('&О программе', self)
        about_action.setStatusTip('Информация о программе')
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def init_toolbar(self):
        toolbar = QToolBar('Основная панель инструментов')
        self.addToolBar(toolbar)

        toolbar.addAction(QIcon.fromTheme('document-new'), 'Новый', self.new_file)
        toolbar.addAction(QIcon.fromTheme('document-open'), 'Открыть', self.open_file)
        toolbar.addAction(QIcon.fromTheme('document-save'), 'Сохранить', self.save_file)
        toolbar.addSeparator()
        toolbar.addAction(QIcon.fromTheme('edit-cut'), 'Вырезать', self.text_edit.cut)
        toolbar.addAction(QIcon.fromTheme('edit-copy'), 'Копировать', self.text_edit.copy)
        toolbar.addAction(QIcon.fromTheme('edit-paste'), 'Вставить', self.text_edit.paste)
        toolbar.addSeparator()
        toolbar.addAction(QIcon.fromTheme('document-print'), 'Печать', self.print_document)

    def new_file(self):
        if self.maybe_save():
            self.text_edit.clear()
            self.current_file = None
            self.setWindowTitle('Блокнот - Новый файл')

    def open_file(self):
        if self.maybe_save():
            file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть файл', '',
                                                       'Текстовые файлы (*.txt);;Все файлы (*)')
            if file_name:
                try:
                    with open(file_name, 'r', encoding='utf-8') as f:
                        self.text_edit.setText(f.read())
                    self.current_file = file_name
                    self.setWindowTitle(f'Блокнот - {file_name}')
                except Exception as e:
                    QMessageBox.warning(self, 'Ошибка', f'Не удалось открыть файл:\n{str(e)}')

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.status_bar.showMessage('Файл успешно сохранен', 2000)
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не удалось сохранить файл:\n{str(e)}')
        else:
            self.save_as_file()

    def save_as_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить как', '',
                                                   'Текстовые файлы (*.txt);;Все файлы (*)')
        if file_name:
            self.current_file = file_name
            self.save_file()
            self.setWindowTitle(f'Блокнот - {file_name}')

    def maybe_save(self):
        if not self.text_edit.document().isModified():
            return True

        ret = QMessageBox.question(self, 'Блокнот',
                                   'Документ был изменен. Сохранить изменения?',
                                   QMessageBox.StandardButton.Save |
                                   QMessageBox.StandardButton.Discard |
                                   QMessageBox.StandardButton.Cancel)

        if ret == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif ret == QMessageBox.StandardButton.Cancel:
            return False

        return True

    def print_document(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)

        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.text_edit.print(printer)

    def about(self):
        QMessageBox.about(self, 'О программе Блокнот',
                          'Простой текстовый редактор (блокнот)\n'
                          'Создан с использованием PyQt6\n'
                          'Версия 1.0\n\n'
                          'Функции:\n'
                          '- Создание, открытие и сохранение текстовых файлов\n'
                          '- Поддержка горячих клавиш\n'
                          '- Печать документов\n'
                          '- Панель инструментов и меню')

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec())