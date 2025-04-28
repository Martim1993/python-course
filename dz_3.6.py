import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLineEdit, QTextEdit, QDateEdit, QComboBox,
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
import sqlite3


class DatabaseManager:

    def __init__(self, db_name='tasks.db'):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_task(self, title, description, due_date, status='pending'):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, description, due_date, status)
                VALUES (?, ?, ?, ?)
            ''', (title, description, due_date, status))
            conn.commit()
            return cursor.lastrowid

    def get_all_tasks(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, description, due_date, status FROM tasks ORDER BY due_date')
            return cursor.fetchall()

    def get_tasks_by_status(self, status):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, description, due_date, status 
                FROM tasks 
                WHERE status = ?
                ORDER BY due_date
            ''', (status,))
            return cursor.fetchall()

    def update_task(self, task_id, title, description, due_date, status):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks 
                SET title = ?, description = ?, due_date = ?, status = ?
                WHERE id = ?
            ''', (title, description, due_date, status, task_id))
            conn.commit()

    def delete_task(self, task_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()

    def mark_as_completed(self, task_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET status = "completed" WHERE id = ?', (task_id,))
            conn.commit()


class TaskManagerApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_task_id = None
        self._setup_ui()
        self._load_tasks()
        self._populate_with_test_data()

    def _setup_ui(self):
        self.setWindowTitle('Менеджер задач')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()

        self.filter_combo = QComboBox()
        self.filter_combo.addItem('Все задачи', 'all')
        self.filter_combo.addItem('Ожидают выполнения', 'pending')
        self.filter_combo.addItem('В процессе', 'in_progress')
        self.filter_combo.addItem('Завершённые', 'completed')
        self.filter_combo.currentIndexChanged.connect(self._load_tasks)

        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self._load_task_details)

        left_layout.addWidget(QLabel('Фильтр по статусу:'))
        left_layout.addWidget(self.filter_combo)
        left_layout.addWidget(QLabel('Список задач:'))
        left_layout.addWidget(self.task_list)

        right_layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText('Название задачи')

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText('Описание задачи')

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDate(QDate.currentDate())

        self.status_combo = QComboBox()
        self.status_combo.addItem('Ожидает выполнения', 'pending')
        self.status_combo.addItem('В процессе', 'in_progress')
        self.status_combo.addItem('Завершено', 'completed')

        button_layout = QHBoxLayout()

        self.add_button = QPushButton('Добавить')
        self.add_button.clicked.connect(self._add_task)

        self.update_button = QPushButton('Обновить')
        self.update_button.clicked.connect(self._update_task)

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self._delete_task)

        self.complete_button = QPushButton('Отметить как выполненную')
        self.complete_button.clicked.connect(self._mark_as_completed)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.complete_button)

        right_layout.addWidget(QLabel('Название задачи:'))
        right_layout.addWidget(self.title_edit)
        right_layout.addWidget(QLabel('Описание:'))
        right_layout.addWidget(self.description_edit)
        right_layout.addWidget(QLabel('Срок выполнения:'))
        right_layout.addWidget(self.due_date_edit)
        right_layout.addWidget(QLabel('Статус:'))
        right_layout.addWidget(self.status_combo)
        right_layout.addLayout(button_layout)

        main_layout.addLayout(left_layout, 40)
        main_layout.addLayout(right_layout, 60)

    def _populate_with_test_data(self):
        tasks = self.db.get_all_tasks()
        if not tasks:
            test_tasks = [
                ('Завершить проект', 'Закончить работу над проектом менеджера задач', '2023-12-31', 'pending'),
                ('Купить продукты', 'Молоко, хлеб, яйца', '2023-11-15', 'completed'),
                ('Записаться к врачу', 'Записаться на прием к стоматологу', '2023-11-20', 'in_progress'),
                ('Прочитать книгу', 'Дочитать "Совершенный код"', '2023-12-01', 'pending'),
                ('Позвонить родителям', 'Обсудить планы на выходные', '2023-11-18', 'completed')
            ]
            for task in test_tasks:
                self.db.add_task(*task)
            self._load_tasks()

    def _load_tasks(self):
        self.task_list.clear()
        filter_status = self.filter_combo.currentData()

        if filter_status == 'all':
            tasks = self.db.get_all_tasks()
        else:
            tasks = self.db.get_tasks_by_status(filter_status)

        for task in tasks:
            task_id, title, _, due_date, status = task
            item_text = f"{title} (до {due_date}) - {self._get_status_text(status)}"
            self.task_list.addItem(item_text)
            self.task_list.item(self.task_list.count() - 1).setData(Qt.ItemDataRole.UserRole, task_id)

    def _get_status_text(self, status):
        status_map = {
            'pending': 'Ожидает',
            'in_progress': 'В процессе',
            'completed': 'Завершено'
        }
        return status_map.get(status, status)

    def _load_task_details(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        task_id = selected_item.data(Qt.ItemDataRole.UserRole)
        tasks = self.db.get_all_tasks()

        for task in tasks:
            if task[0] == task_id:
                self.current_task_id = task_id
                self.title_edit.setText(task[1])
                self.description_edit.setPlainText(task[2])

                due_date = QDate.fromString(task[3], 'yyyy-MM-dd')
                self.due_date_edit.setDate(due_date)

                index = self.status_combo.findData(task[4])
                if index >= 0:
                    self.status_combo.setCurrentIndex(index)
                break

    def _clear_form(self):
        self.current_task_id = None
        self.title_edit.clear()
        self.description_edit.clear()
        self.due_date_edit.setDate(QDate.currentDate())
        self.status_combo.setCurrentIndex(0)

    def _add_task(self):
        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, 'Ошибка', 'Название задачи обязательно!')
            return

        description = self.description_edit.toPlainText().strip()
        due_date = self.due_date_edit.date().toString('yyyy-MM-dd')
        status = self.status_combo.currentData()

        self.db.add_task(title, description, due_date, status)
        self._clear_form()
        self._load_tasks()
        QMessageBox.information(self, 'Успех', 'Задача успешно добавлена!')

    def _update_task(self):
        if not self.current_task_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите задачу для редактирования!')
            return

        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, 'Ошибка', 'Название задачи обязательно!')
            return

        description = self.description_edit.toPlainText().strip()
        due_date = self.due_date_edit.date().toString('yyyy-MM-dd')
        status = self.status_combo.currentData()

        self.db.update_task(self.current_task_id, title, description, due_date, status)
        self._load_tasks()
        QMessageBox.information(self, 'Успех', 'Задача успешно обновлена!')

    def _delete_task(self):
        if not self.current_task_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите задачу для удаления!')
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить эту задачу?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_task(self.current_task_id)
            self._clear_form()
            self._load_tasks()
            QMessageBox.information(self, 'Успех', 'Задача успешно удалена!')

    def _mark_as_completed(self):
        if not self.current_task_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите задачу для отметки!')
            return

        self.db.mark_as_completed(self.current_task_id)
        self._load_tasks()
        self._load_task_details()  # Обновляем форму, чтобы отразить новый статус
        QMessageBox.information(self, 'Успех', 'Задача отмечена как выполненная!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec())
