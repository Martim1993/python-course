import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QFileDialog, QMessageBox)
from PyQt6.QtGui import QPixmap, QImage, QAction, QPainter, QPageSize
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtCore import Qt


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр и печать изображений")
        self.setGeometry(100, 100, 800, 600)

        # Основные виджеты
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0;")

        self.load_button = QPushButton("Загрузить изображение")
        self.load_button.clicked.connect(self.load_image)

        self.print_button = QPushButton("Печать")
        self.print_button.clicked.connect(self.print_image)
        self.print_button.setEnabled(False)

        # Размещение виджетов
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.print_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Создаем меню
        self.create_menu()

        # Текущее изображение
        self.current_image = None

    def create_menu(self):
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("&Файл")

        load_action = QAction("Загрузить изображение", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)

        print_action = QAction("Печать", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_image)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_image(self):
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.jpg *.jpeg *.png);;Все файлы (*)"
        )

        if file_path:
            try:
                # Загружаем изображение
                pixmap = QPixmap(file_path)

                if pixmap.isNull():
                    raise ValueError("Не удалось загрузить изображение")

                # Масштабируем для отображения
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size() * 0.9,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )

                self.image_label.setPixmap(scaled_pixmap)
                self.current_image = pixmap
                self.print_button.setEnabled(True)

                # Обновляем статус
                self.statusBar().showMessage(f"Загружено: {file_path}", 3000)

            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    f"Не удалось загрузить изображение:\n{str(e)}"
                )

    def print_image(self):
        if not self.current_image or self.current_image.isNull():
            QMessageBox.warning(self, "Ошибка", "Нет изображения для печати")
            return

        # Создаем принтер и диалог печати
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))

        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            try:
                # Создаем painter для печати
                painter = QPainter()
                painter.begin(printer)

                # Получаем размеры страницы и изображения
                page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
                image_rect = self.current_image.rect()

                # Масштабируем изображение для печати
                scale = min(
                    page_rect.width() / image_rect.width(),
                    page_rect.height() / image_rect.height()
                )

                # Центрируем изображение
                x = (page_rect.width() - image_rect.width() * scale) / 2
                y = (page_rect.height() - image_rect.height() * scale) / 2

                # Рисуем изображение
                painter.drawPixmap(
                    x, y,
                    image_rect.width() * scale,
                    image_rect.height() * scale,
                    self.current_image
                )

                painter.end()

                self.statusBar().showMessage("Изображение отправлено на печать", 3000)

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка печати",
                    f"Не удалось распечатать изображение:\n{str(e)}"
                )

    def resizeEvent(self, event):
        # При изменении размера окна масштабируем изображение
        if self.current_image and not self.current_image.isNull():
            scaled_pixmap = self.current_image.scaled(
                self.image_label.size() * 0.9,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())