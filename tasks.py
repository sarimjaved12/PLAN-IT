from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QComboBox, QHBoxLayout
from PyQt6.QtCore import Qt
import json
import os

tasks_file = 'tasks.json'

def load_tasks(username):
    try:
        with open(tasks_file, 'r') as file:
            tasks = json.load(file)
            return tasks.get(username, [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_tasks(username, tasks):
    all_tasks = {}
    try:
        with open(tasks_file, 'r') as file:
            all_tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    all_tasks[username] = tasks
    with open(tasks_file, 'w') as file:
        json.dump(all_tasks, file, indent=4)

class TaskManager(QMainWindow):
    def __init__(self, username, auth_window):
        super().__init__()
        self.username = username
        self.auth_window = auth_window
        self.tasks = load_tasks(self.username)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PLAN-IT - Task Manager")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #FDEE00;")

        self.layout = QVBoxLayout()

        self.title_label = QLabel("TASK MANAGER", self)
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.layout.addWidget(self.title_label)

        self.title_entry = QLineEdit(self)
        self.title_entry.setPlaceholderText("Task Title")
        self.title_entry.setStyleSheet("font-weight: bold; color: black;")
        self.layout.addWidget(self.title_entry)

        self.description_entry = QLineEdit(self)
        self.description_entry.setPlaceholderText("Description")
        self.description_entry.setStyleSheet("font-weight: bold; color: black;")
        self.layout.addWidget(self.description_entry)

        self.due_date_entry = QLineEdit(self)
        self.due_date_entry.setPlaceholderText("Due Date (YYYY-MM-DD)")
        self.due_date_entry.setStyleSheet("font-weight: bold; color: black;")
        self.layout.addWidget(self.due_date_entry)

        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setStyleSheet("font-weight: bold; color: black;")
        self.layout.addWidget(self.priority_combo)

        self.add_task_button = QPushButton("Add Task", self)
        self.add_task_button.setStyleSheet("font-weight: bold; color: black;")
        self.add_task_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_task_button)

        self.task_list = QListWidget(self)
        self.layout.addWidget(self.task_list)
        self.refresh_task_list()

        self.remove_task_button = QPushButton("Remove Selected Task", self)
        self.remove_task_button.setStyleSheet("font-weight: bold; color: black;")
        self.remove_task_button.clicked.connect(self.remove_task)
        self.layout.addWidget(self.remove_task_button)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet("font-weight: bold; color: black;")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def add_task(self):
        title = self.title_entry.text()
        description = self.description_entry.text()
        due_date = self.due_date_entry.text()
        priority = self.priority_combo.currentText()

        if not title or not due_date or not priority:
            QMessageBox.critical(self, "Error", "Please fill in all required fields.")
            return

        task = {"title": title, "description": description, "due_date": due_date, "priority": priority}
        self.tasks.append(task)
        save_tasks(self.username, self.tasks)
        self.refresh_task_list()

    def remove_task(self):
        selected_task = self.task_list.currentRow()
        if selected_task == -1:
            QMessageBox.critical(self, "Error", "Please select a task to remove.")
            return

        del self.tasks[selected_task]
        save_tasks(self.username, self.tasks)
        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            self.task_list.addItem(f"{task['title']} - {task['due_date']} ({task['priority']})")

    def logout(self):
        self.close()
        self.auth_window.show()