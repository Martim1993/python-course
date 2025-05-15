import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QSlider,
                             QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                             QPushButton, QMessageBox, QListWidget, QStyle)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QSettings, QUrl, QTimer, QSize
from PyQt6.QtGui import QKeySequence, QShortcut, QIcon


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setMinimumSize(800, 600)

        # Сначала создаем ВСЕ виджеты
        self.video_widget = QVideoWidget()  # <-- Создаем первым!
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)  # 50% громкости
        self.media_player.setAudioOutput(self.audio_output)

        # Затем настраиваем связи между ними
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        # Инициализация UI
        self.init_ui()

        # Настройки
        self.settings = QSettings("VideoPlayer", "VideoPlayerApp")
        self.load_settings()

        # Таймеры и другие свойства
        self.position_timer = QTimer(self)
        self.position_timer.setInterval(100)
        self.position_timer.timeout.connect(self.update_position)

        self.playlist = []
        self.current_media_index = -1

        self.apply_styles()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создание виджетов
        self.create_widgets()

        # Настройка компоновки
        self.setup_layout(central_widget)

        # Подключение сигналов
        self.connect_signals()

        # Настройка горячих клавиш
        self.setup_shortcuts()

    def create_widgets(self):
        """Создание виджетов интерфейса"""
        # Кнопки управления
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.setFixedSize(40, 40)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))
        self.stop_button.setFixedSize(40, 40)

        self.mute_button = QPushButton()
        self.mute_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        self.mute_button.setFixedSize(40, 40)
        self.mute_button.setCheckable(True)

        self.open_button = QPushButton("Open")
        self.open_button.setFixedSize(80, 40)

        # Слайдеры
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.setSingleStep(1000)  # Шаг 1 секунда

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setFixedWidth(100)

        # Метки
        self.time_label = QLabel("00:00 / 00:00")
        self.status_label = QLabel("Ready")

        # Плейлист
        self.playlist_widget = QListWidget()
        self.playlist_widget.setAlternatingRowColors(True)

    def setup_layout(self, central_widget):
        """Настройка компоновки интерфейса"""
        # Панель управления
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.mute_button)
        control_layout.addWidget(self.volume_slider)
        control_layout.addWidget(self.open_button)
        control_layout.addStretch()
        control_layout.addWidget(self.status_label)

        # Основная компоновка
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_widget, 4)
        main_layout.addWidget(self.position_slider)
        main_layout.addWidget(self.time_label)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(QLabel("Playlist:"))
        main_layout.addWidget(self.playlist_widget, 2)

        central_widget.setLayout(main_layout)

    def connect_signals(self):
        """Подключение сигналов к слотам"""
        # Кнопки
        self.play_button.clicked.connect(self.play_pause)
        self.stop_button.clicked.connect(self.stop)
        self.mute_button.toggled.connect(self.toggle_mute)
        self.open_button.clicked.connect(self.open_files)

        # Слайдеры
        self.position_slider.sliderMoved.connect(self.set_position)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Медиаплеер
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.playbackStateChanged.connect(self.update_buttons)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.errorOccurred.connect(self.handle_error)

        # Плейлист
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected_item)

    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        QShortcut(QKeySequence("Space"), self).activated.connect(self.play_pause)
        QShortcut(QKeySequence("Right"), self).activated.connect(self.seek_forward)
        QShortcut(QKeySequence("Left"), self).activated.connect(self.seek_backward)
        QShortcut(QKeySequence("M"), self).activated.connect(self.toggle_mute_key)

    def load_settings(self):
        """Загрузка сохраненных настроек"""
        # Геометрия окна
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))

        # Громкость
        volume = self.settings.value("volume", 50, int)
        self.audio_output.setVolume(volume / 100)
        self.volume_slider.setValue(volume)

        # Состояние звука
        mute = self.settings.value("mute", False, bool)
        self.audio_output.setMuted(mute)
        self.mute_button.setChecked(mute)
        self.update_mute_icon()

    def save_settings(self):
        """Сохранение текущих настроек"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("volume", self.volume_slider.value())
        self.settings.setValue("mute", self.audio_output.isMuted())

    def apply_styles(self):
        """Применение стилей к приложению"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            QPushButton:checked {
                background-color: #1a6b9a;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #3a3a3a;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #e0e0e0;
                border: 1px solid #555;
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::sub-page:horizontal {
                background: #1a6b9a;
            }
            QListWidget {
                background-color: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #555;
                alternate-background-color: #353535;
            }
            QLabel {
                color: #e0e0e0;
            }
        """)

    # Основные функции управления видео
    def open_files(self):
        """Открытие файлов через диалоговое окно"""
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi *.mkv *.mov)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.add_to_playlist(selected_files)

            if not self.media_player.source().isValid() and selected_files:
                self.current_media_index = 0
                self.load_media(self.playlist[0])

    def add_to_playlist(self, files):
        """Добавление файлов в плейлист"""
        for file in files:
            if file not in self.playlist:
                self.playlist.append(file)
                self.playlist_widget.addItem(file.split('/')[-1])
        self.status_label.setText(f"Added {len(files)} files to playlist")

    def play_selected_item(self, item):
        """Воспроизведение выбранного элемента плейлиста"""
        index = self.playlist_widget.row(item)
        if 0 <= index < len(self.playlist):
            self.current_media_index = index
            self.load_media(self.playlist[index])

    def load_media(self, file_path):
        """Загрузка медиафайла"""
        try:
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.status_label.setText(f"Playing: {file_path.split('/')[-1]}")
            self.play()
        except Exception as e:
            self.status_label.setText("Error loading file")
            QMessageBox.warning(self, "Error", f"Could not load file:\n{str(e)}")

    def play_pause(self):
        """Переключение между воспроизведением и паузой"""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
        else:
            self.play()

    def play(self):
        """Начать воспроизведение"""
        if self.media_player.source().isValid():
            self.media_player.play()
            self.position_timer.start()
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def pause(self):
        """Поставить на паузу"""
        self.media_player.pause()
        self.position_timer.stop()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def stop(self):
        """Остановить воспроизведение"""
        self.media_player.stop()
        self.position_timer.stop()
        self.position_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.status_label.setText("Stopped")

    def set_position(self, position):
        """Установка позиции воспроизведения"""
        self.media_player.setPosition(position)

    def set_volume(self, volume):
        """Установка уровня громкости (0-100)"""
        self.audio_output.setVolume(volume / 100)
        self.update_mute_icon()

    def toggle_mute(self, muted):
        """Переключение состояния звука"""
        self.audio_output.setMuted(muted)
        self.update_mute_icon()

    def toggle_mute_key(self):
        """Переключение звука по горячей клавише"""
        self.mute_button.toggle()

    def update_mute_icon(self):
        """Обновление иконки кнопки mute"""
        if self.audio_output.isMuted() or self.audio_output.volume() == 0:
            self.mute_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
        else:
            self.mute_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))

    # Функции перемотки
    def seek_forward(self):
        """Перемотка вперед на 5 секунд"""
        if self.media_player.isPlaying():
            new_pos = min(
                self.media_player.position() + 5000,
                self.media_player.duration()
            )
            self.media_player.setPosition(new_pos)

    def seek_backward(self):
        """Перемотка назад на 5 секунд"""
        if self.media_player.isPlaying():
            new_pos = max(
                self.media_player.position() - 5000,
                0
            )
            self.media_player.setPosition(new_pos)

    # Обновление интерфейса
    def update_buttons(self, state):
        """Обновление состояния кнопок"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def update_duration(self, duration):
        """Обновление длительности видео"""
        self.position_slider.setRange(0, duration)
        self.update_time_label(self.media_player.position(), duration)

    def update_position(self):
        """Обновление текущей позиции"""
        if not self.position_slider.isSliderDown():
            self.position_slider.setValue(self.media_player.position())

        self.update_time_label(self.media_player.position(), self.media_player.duration())

    def update_time_label(self, position, duration):
        """Обновление метки времени"""
        position_time = self.format_time(position)
        duration_time = self.format_time(duration)
        self.time_label.setText(f"{position_time} / {duration_time}")

    def format_time(self, milliseconds):
        """Форматирование времени в MM:SS"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    # Обработка ошибок
    def handle_error(self):
        """Обработка ошибок воспроизведения"""
        error = self.media_player.error()
        if error != QMediaPlayer.Error.NoError:
            self.status_label.setText("Error occurred")
            QMessageBox.warning(self, "Error", self.media_player.errorString())
            self.stop()

    def closeEvent(self, event):
        """Обработка события закрытия окна"""
        self.save_settings()
        self.media_player.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Современный стиль для всех платформ

    player = VideoPlayer()
    player.show()

    sys.exit(app.exec())