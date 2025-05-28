import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QPushButton, QTextEdit, QComboBox, QSlider,
                             QVBoxLayout, QHBoxLayout, QMenuBar,
                             QMdiArea, QMdiSubWindow, QMessageBox, QCheckBox)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Многооконное приложение")
        self.setGeometry(100, 100, 800, 600)

        # Создаем MDI область для управления подокнами
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        # Создаем 5 разных окон
        self.create_windows()

        # Создаем меню
        self.create_menu()

    def create_windows(self):
        """Создаем 5 разных окон с различными виджетами"""
        # Окно 1 - Текстовое
        self.window1 = QMdiSubWindow()
        self.window1.setWidget(TextWindow("Текстовое окно"))
        self.window1.setWindowTitle("Текстовое окно")

        # Окно 2 - Кнопки
        self.window2 = QMdiSubWindow()
        self.window2.setWidget(ButtonsWindow("Окно с кнопками"))
        self.window2.setWindowTitle("Окно с кнопками")

        # Окно 3 - Выбор
        self.window3 = QMdiSubWindow()
        self.window3.setWidget(SelectionWindow("Окно выбора"))
        self.window3.setWindowTitle("Окно выбора")

        # Окно 4 - Слайдер
        self.window4 = QMdiSubWindow()
        self.window4.setWidget(SliderWindow("Окно со слайдером"))
        self.window4.setWindowTitle("Окно со слайдером")

        # Окно 5 - Комбинированное
        self.window5 = QMdiSubWindow()
        self.window5.setWidget(CombinedWindow("Комбинированное окно"))
        self.window5.setWindowTitle("Комбинированное окно")

        # Добавляем все окна в MDI область
        self.mdi.addSubWindow(self.window1)
        self.mdi.addSubWindow(self.window2)
        self.mdi.addSubWindow(self.window3)
        self.mdi.addSubWindow(self.window4)
        self.mdi.addSubWindow(self.window5)

        # Располагаем окна каскадом
        self.mdi.cascadeSubWindows()

    def create_menu(self):
        """Создаем главное меню"""
        menubar = self.menuBar()

        # Меню "Окна"
        window_menu = menubar.addMenu("&Окна")

        # Действия для переключения между окнами
        show_window1 = QAction("Текстовое окно", self)
        show_window1.triggered.connect(lambda: self.activate_window(self.window1))
        window_menu.addAction(show_window1)

        show_window2 = QAction("Окно с кнопками", self)
        show_window2.triggered.connect(lambda: self.activate_window(self.window2))
        window_menu.addAction(show_window2)

        show_window3 = QAction("Окно выбора", self)
        show_window3.triggered.connect(lambda: self.activate_window(self.window3))
        window_menu.addAction(show_window3)

        show_window4 = QAction("Окно со слайдером", self)
        show_window4.triggered.connect(lambda: self.activate_window(self.window4))
        window_menu.addAction(show_window4)

        show_window5 = QAction("Комбинированное окно", self)
        show_window5.triggered.connect(lambda: self.activate_window(self.window5))
        window_menu.addAction(show_window5)

        window_menu.addSeparator()

        # Действия для изменения расположения окон
        cascade_action = QAction("Каскадом", self)
        cascade_action.triggered.connect(self.mdi.cascadeSubWindows)
        window_menu.addAction(cascade_action)

        tile_action = QAction("Мозаикой", self)
        tile_action.triggered.connect(self.mdi.tileSubWindows)
        window_menu.addAction(tile_action)

        # Меню "Файл"
        file_menu = menubar.addMenu("&Файл")

        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def activate_window(self, window):
        """Активируем указанное окно"""
        window.showNormal()
        window.setFocus()

    def closeEvent(self, event):
        """Обработка события закрытия приложения"""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы действительно хотите выйти?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


# Классы для разных окон приложения
class TextWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Это текстовое окно. Введите текст ниже:")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)


class ButtonsWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Это окно с кнопками:")
        layout.addWidget(self.label)

        self.button1 = QPushButton("Кнопка 1")
        self.button2 = QPushButton("Кнопка 2")
        self.button3 = QPushButton("Кнопка 3")

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.button1.clicked.connect(lambda: self.button_clicked(1))
        self.button2.clicked.connect(lambda: self.button_clicked(2))
        self.button3.clicked.connect(lambda: self.button_clicked(3))

    def button_clicked(self, num):
        print(f"Нажата кнопка {num}")


class SelectionWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Это окно с элементами выбора:")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["Вариант 1", "Вариант 2", "Вариант 3"])
        layout.addWidget(self.combo)

        self.checkbox = QCheckBox("Выбрать")
        layout.addWidget(self.checkbox)

        self.combo.currentIndexChanged.connect(self.selection_changed)
        self.checkbox.stateChanged.connect(self.checkbox_changed)

    def selection_changed(self, index):
        print(f"Выбран вариант {index + 1}")

    def checkbox_changed(self, state):
        print(f"Чекбокс {'выбран' if state else 'не выбран'}")


class SliderWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Это окно со слайдером:")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        layout.addWidget(self.slider)

        self.value_label = QLabel(f"Текущее значение: {self.slider.value()}")
        layout.addWidget(self.value_label)

        self.slider.valueChanged.connect(self.slider_changed)

    def slider_changed(self, value):
        self.value_label.setText(f"Текущее значение: {value}")


class CombinedWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)

        layout = QHBoxLayout()
        self.setLayout(layout)

        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)

        self.label = QLabel("Комбинированное окно с разными виджетами")
        left_panel.addWidget(self.label)

        self.text_edit = QTextEdit()
        left_panel.addWidget(self.text_edit)

        self.button = QPushButton("Нажми меня")
        right_panel.addWidget(self.button)

        self.slider = QSlider(Qt.Orientation.Vertical)
        right_panel.addWidget(self.slider)

        self.button.clicked.connect(self.button_clicked)
        self.slider.valueChanged.connect(self.slider_changed)

    def button_clicked(self):
        print("Кнопка нажата")

    def slider_changed(self, value):
        print(f"Значение слайдера: {value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())