import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
                             QPushButton, QColorDialog, QFontDialog, QTextEdit,
                             QFileDialog, QSystemTrayIcon, QMenu, QMessageBox)
from PyQt6.QtGui import QColor, QFont, QAction, QIcon
from PyQt6.QtCore import QSettings, QDateTime, Qt


class SettingsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение с настройками")
        self.setGeometry(100, 100, 600, 500)

        # Инициализация настроек
        self.settings = QSettings("MyCompany", "SettingsApp")
        self.load_settings()

        # Создаем системный трей
        self.create_system_tray()

        # Основные виджеты
        self.init_ui()

        # Применяем загруженные настройки
        self.apply_settings()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Виджет для отображения текста
        self.label = QLabel("Пример текста для демонстрации настроек")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Виджет для отображения содержимого файла
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # Кнопки для настроек
        self.bg_color_btn = QPushButton("Изменить цвет фона")
        self.bg_color_btn.clicked.connect(self.change_bg_color)
        layout.addWidget(self.bg_color_btn)

        self.font_btn = QPushButton("Изменить шрифт")
        self.font_btn.clicked.connect(self.change_font)
        layout.addWidget(self.font_btn)

        self.load_file_btn = QPushButton("Загрузить текстовый файл")
        self.load_file_btn.clicked.connect(self.load_text_file)
        layout.addWidget(self.load_file_btn)

        self.save_settings_btn = QPushButton("Сохранить настройки")
        self.save_settings_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_settings_btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("preferences-system"))

        tray_menu = QMenu()
        show_action = QAction("Показать", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def change_bg_color(self):
        color = QColorDialog.getColor(initial=QColor(self.bg_color), parent=self,
                                      title="Выберите цвет фона")
        if color.isValid():
            self.bg_color = color.name()
            self.apply_settings()

    def change_font(self):
        font, ok = QFontDialog.getFont(QFont(self.font_family, self.font_size),
                                       self, "Выберите шрифт")
        if ok:
            self.font_family = font.family()
            self.font_size = font.pointSize()
            self.apply_settings()

    def load_text_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть текстовый файл", "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)

                # Показываем уведомление в трее
                self.tray_icon.showMessage(
                    "Файл загружен",
                    f"Файл {file_path} успешно загружен",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000
                )

                # Сохраняем путь к последнему файлу
                self.last_file = file_path

            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}")

    def save_settings(self):
        # Сохраняем настройки
        self.settings.setValue("bg_color", self.bg_color)
        self.settings.setValue("font_family", self.font_family)
        self.settings.setValue("font_size", self.font_size)
        self.settings.setValue("last_file", self.last_file)

        # Для Windows сохраняем дополнительные данные в реестр
        self.settings.setValue("user_name", "Current User")
        self.settings.setValue("last_run", QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate))

        # Уведомление
        self.tray_icon.showMessage(
            "Настройки сохранены",
            "Ваши настройки были успешно сохранены",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def load_settings(self):
        # Загружаем настройки или устанавливаем значения по умолчанию
        self.bg_color = self.settings.value("bg_color", "#ffffff")
        self.font_family = self.settings.value("font_family", "Arial")
        self.font_size = int(self.settings.value("font_size", 12))
        self.last_file = self.settings.value("last_file", "")

        # Для Windows загружаем дополнительные данные из реестра
        self.user_name = self.settings.value("user_name", "Гость")
        self.last_run = self.settings.value("last_run", "Неизвестно")

    def apply_settings(self):
        # Применяем настройки к интерфейсу
        self.setStyleSheet(f"background-color: {self.bg_color};")

        font = QFont(self.font_family, self.font_size)
        self.label.setFont(font)
        self.text_edit.setFont(font)

    def close_app(self):
        # Сохраняем настройки перед выходом
        self.save_settings()
        self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event):
        # При закрытии окна сворачиваем в трей
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Приложение свернуто",
            "Приложение продолжает работать в системном трее",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Убедимся, что QApplication создан до QSettings
    if sys.platform == "win32":
        QSettings.setDefaultFormat(QSettings.Format.NativeFormat)

    window = SettingsApp()
    window.show()
    sys.exit(app.exec())